"""Unit tests for the sensor clients' HTTP handling, using a mocked transport."""

import json
from datetime import datetime, timezone
from typing import Any

import httpx
import pytest
from pytest_httpx import HTTPXMock

from irls import AsyncIRLSClient, IRLSClient
from irls.dto import CTDSensorReadingDTO, PositionSensorReadingDTO
from irls.exceptions import (
    APIDisabledError,
    RequestError,
    SensorDisabledError,
    SensorNotFoundError,
    ValidationError,
)

BASE_URL = "http://irls.test"
RECORDED_AT = datetime(2025, 12, 7, 19, 0, 0, 123000, tzinfo=timezone.utc)

POSITION = PositionSensorReadingDTO(recorded_at=RECORDED_AT, x=-123.1, y=48.4, altitude=-512.0)
CTD = CTDSensorReadingDTO(
    recorded_at=RECORDED_AT, temperature=4.82, conductivity=3.12, pressure=512.5
)

# (sensor type in the URL, client attribute, reading)
SENSORS = [
    pytest.param("position", "position", POSITION, id="position"),
    pytest.param("ctd", "ctd", CTD, id="ctd"),
]


def send(kind: str, data: Any, slug: str = "rovins") -> Any:
    return getattr(IRLSClient(base_url=BASE_URL), kind).send(sensor_slug=slug, data=data)


async def send_async(kind: str, data: Any, slug: str = "rovins") -> Any:
    return await getattr(AsyncIRLSClient(base_url=BASE_URL), kind).send(sensor_slug=slug, data=data)


@pytest.mark.parametrize("path, kind, data", SENSORS)
def test_send_posts_json_and_returns_response(
    httpx_mock: HTTPXMock, path: str, kind: str, data: Any
) -> None:
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/api/sensors/{path}/rovins/data",
        status_code=201,
        json={"message": "Reading stored successfully", "id": 42},
    )

    response = send(kind, data)

    assert response.id == 42
    request = httpx_mock.get_request()
    assert request is not None
    assert request.headers["accept"] == "application/json"
    body = json.loads(request.content)
    assert body["recorded_at"] == "2025-12-07T19:00:00.123Z"
    assert all(value is not None for value in body.values())


@pytest.mark.parametrize("path, kind, data", SENSORS)
async def test_async_send_returns_response(
    httpx_mock: HTTPXMock, path: str, kind: str, data: Any
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/sensors/{path}/rovins/data",
        status_code=201,
        json={"message": "Reading stored successfully", "id": 7},
    )

    response = await send_async(kind, data)

    assert response.id == 7


ERRORS = [
    pytest.param(
        404,
        {"message": "No query results for model [App\\Models\\Sensors\\PositionSensor] nope."},
        SensorNotFoundError,
        id="unknown-sensor",
    ),
    pytest.param(404, {"message": "Not Found"}, APIDisabledError, id="api-disabled"),
    pytest.param(403, {"message": "Sensor is disabled"}, SensorDisabledError, id="disabled"),
    pytest.param(
        422,
        {"message": "The x field is required.", "errors": {"x": ["The x field is required."]}},
        ValidationError,
        id="validation",
    ),
    pytest.param(500, {"message": "Server Error"}, RequestError, id="server-error"),
]


@pytest.mark.parametrize("path, kind, data", SENSORS)
@pytest.mark.parametrize("status, body, error", ERRORS)
def test_send_maps_error_responses(
    httpx_mock: HTTPXMock,
    path: str,
    kind: str,
    data: Any,
    status: int,
    body: dict[str, Any],
    error: type[Exception],
) -> None:
    httpx_mock.add_response(status_code=status, json=body)

    with pytest.raises(error):
        send(kind, data, slug="nope")


@pytest.mark.parametrize("path, kind, data", SENSORS)
@pytest.mark.parametrize("status, body, error", ERRORS)
async def test_async_send_maps_error_responses(
    httpx_mock: HTTPXMock,
    path: str,
    kind: str,
    data: Any,
    status: int,
    body: dict[str, Any],
    error: type[Exception],
) -> None:
    httpx_mock.add_response(status_code=status, json=body)

    with pytest.raises(error):
        await send_async(kind, data, slug="nope")


def test_validation_error_carries_field_errors(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        status_code=422,
        json={"message": "Invalid", "errors": {"heading": ["Must be between 0 and 360."]}},
    )

    with pytest.raises(ValidationError) as exc_info:
        send("position", POSITION)

    assert exc_info.value.errors == {"heading": ["Must be between 0 and 360."]}


@pytest.mark.parametrize("path, kind, data", SENSORS)
def test_send_wraps_timeouts(httpx_mock: HTTPXMock, path: str, kind: str, data: Any) -> None:
    httpx_mock.add_exception(httpx.ReadTimeout("timed out"))

    with pytest.raises(RequestError, match="timed out"):
        send(kind, data)


@pytest.mark.parametrize("path, kind, data", SENSORS)
def test_send_wraps_connection_errors(
    httpx_mock: HTTPXMock, path: str, kind: str, data: Any
) -> None:
    httpx_mock.add_exception(httpx.ConnectError("connection refused"))

    with pytest.raises(RequestError, match="connection refused"):
        send(kind, data)
