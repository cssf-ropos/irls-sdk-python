"""Round-trip tests against a running IRLS 3.0.

Skipped unless IRLS_URL is set. The target needs the sensors from irls-3's
LocalSensorSeeder (rovins, disabled-gps, ctd); irls-home's `bin/test e2e`
starts a throwaway instance with them.
"""

import os
from datetime import datetime, timezone

import pytest

from irls import AsyncIRLSClient, IRLSClient
from irls.dto import CTDSensorReadingDTO, ExtraMeasurementDTO, PositionSensorReadingDTO
from irls.exceptions import SensorDisabledError, SensorNotFoundError, ValidationError

IRLS_URL = os.environ.get("IRLS_URL")

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not IRLS_URL, reason="set IRLS_URL to run against a live IRLS"),
]


@pytest.fixture
def client() -> IRLSClient:
    assert IRLS_URL
    return IRLSClient(base_url=IRLS_URL, timeout=10.0)


def position() -> PositionSensorReadingDTO:
    return PositionSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        x=-123.3656,
        y=48.4284,
        altitude=-512.3,
        heading=45.2,
        pitch=2.1,
        roll=-1.5,
        raw_data={"source": "irls-sdk integration test"},
    )


def test_position_reading_is_stored(client: IRLSClient) -> None:
    response = client.position.send(sensor_slug="rovins", data=position())

    assert response.id > 0


async def test_async_position_reading_is_stored() -> None:
    assert IRLS_URL
    client = AsyncIRLSClient(base_url=IRLS_URL, timeout=10.0)

    response = await client.position.send(sensor_slug="rovins", data=position())

    assert response.id > 0


def test_ctd_reading_with_extra_measurements_is_stored(client: IRLSClient) -> None:
    reading = CTDSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        temperature=4.82,
        conductivity=3.12,
        pressure=512.5,
        salinity=34.89,
        extra_measurements=[
            ExtraMeasurementDTO(name="fluorescence", value=0.18, unit="micrograms_per_litre")
        ],
    )

    response = client.ctd.send(sensor_slug="ctd", data=reading)

    assert response.id > 0


def test_unknown_sensor_raises_not_found(client: IRLSClient) -> None:
    with pytest.raises(SensorNotFoundError):
        client.position.send(sensor_slug="no-such-sensor", data=position())


def test_disabled_sensor_raises_disabled(client: IRLSClient) -> None:
    with pytest.raises(SensorDisabledError):
        client.position.send(sensor_slug="disabled-gps", data=position())


def test_out_of_range_heading_is_rejected_by_the_server(client: IRLSClient) -> None:
    # Bypass the DTO's own range check so the server-side validation is exercised.
    reading = position().model_copy(update={"heading": 400.0})

    with pytest.raises(ValidationError) as exc_info:
        client.position.send(sensor_slug="rovins", data=reading)

    assert "heading" in exc_info.value.errors
