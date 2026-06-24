"""Unit tests for CTD DTOs - no API required."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from irls.dto import CTDSensorReadingDTO, ExtraMeasurementDTO


def test_ctd_reading_minimal():
    reading = CTDSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        temperature=4.82,
        conductivity=3.12,
        pressure=512.5,
    )

    assert reading.temperature == 4.82
    assert reading.conductivity == 3.12
    assert reading.pressure == 512.5
    assert reading.salinity is None
    assert reading.extra_measurements is None


def test_ctd_reading_full():
    reading = CTDSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        temperature=4.82,
        conductivity=3.12,
        pressure=512.5,
        salinity=34.89,
        dissolved_oxygen=298.4,
        sound_velocity=1490.3,
        turbidity=0.21,
        density=1027.6,
        status="OK",
        raw_data={"firmware": "3.2.5", "message_id": 48291},
    )

    assert reading.salinity == 34.89
    assert reading.dissolved_oxygen == 298.4
    assert reading.status == "OK"
    assert reading.raw_data == {"firmware": "3.2.5", "message_id": 48291}


def test_ctd_reading_with_extra_measurements():
    reading = CTDSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        temperature=4.82,
        conductivity=3.12,
        pressure=512.5,
        extra_measurements=[
            ExtraMeasurementDTO(name="fluorescence", value=0.18, unit="micrograms_per_litre"),
            ExtraMeasurementDTO(name="par", value=0.4, unit="micromol_photons_per_m2_per_s"),
            ExtraMeasurementDTO(name="ph", value=7.92, unit="ph"),
        ],
    )

    assert len(reading.extra_measurements) == 3
    assert reading.extra_measurements[0].name == "fluorescence"
    assert reading.extra_measurements[0].unit == "micrograms_per_litre"


def test_ctd_reading_negative_pressure_rejected():
    with pytest.raises(ValidationError) as exc_info:
        CTDSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            temperature=4.82,
            conductivity=3.12,
            pressure=-1.0,
        )

    assert "pressure" in str(exc_info.value)


def test_ctd_reading_missing_required_fields():
    with pytest.raises(ValidationError) as exc_info:
        CTDSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            temperature=4.82,
            # missing conductivity and pressure
        )

    errors = str(exc_info.value)
    assert "conductivity" in errors


def test_extra_measurement_invalid_unit():
    with pytest.raises(ValidationError) as exc_info:
        ExtraMeasurementDTO(name="foo", value=1.0, unit="not_a_real_unit")

    assert "unit" in str(exc_info.value)


def test_ctd_reading_json_serialization():
    reading = CTDSensorReadingDTO(
        recorded_at=datetime(2026, 6, 23, 14, 0, 0, 123000, tzinfo=timezone.utc),
        temperature=4.82,
        conductivity=3.12,
        pressure=512.5,
        extra_measurements=[
            ExtraMeasurementDTO(name="fluorescence", value=0.18, unit="micrograms_per_litre"),
        ],
    )

    payload = reading.model_dump(mode="json", exclude_none=True)

    assert payload["temperature"] == 4.82
    assert payload["conductivity"] == 3.12
    assert payload["pressure"] == 512.5
    assert "recorded_at" in payload
    assert len(payload["extra_measurements"]) == 1
    assert payload["extra_measurements"][0]["unit"] == "micrograms_per_litre"
    assert "salinity" not in payload  # excluded because None
