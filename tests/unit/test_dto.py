"""Unit tests for DTOs - no API required."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from irls.dto import PositionSensorReadingDTO, SensorReadingResponse


def test_position_sensor_reading_minimal():
    """Test creating a minimal position sensor reading."""
    reading = PositionSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        x=-122.4194,
        y=37.7749,
        altitude=10.5,
    )

    assert reading.x == -122.4194
    assert reading.y == 37.7749
    assert reading.altitude == 10.5
    assert reading.heading is None  # Optional field


def test_position_sensor_reading_full():
    """Test creating a full position sensor reading with all fields."""
    recorded_at = datetime.now(timezone.utc)

    reading = PositionSensorReadingDTO(
        recorded_at=recorded_at,
        x=-122.4194,
        y=37.7749,
        altitude=10.5,
        heading=45.2,
        pitch=2.1,
        roll=-1.5,
        speed=5.3,
        satellite_count=12,
        hdop=1.2,
        status="GPS_FIX",
        raw_data={"test": "data"},
    )

    assert reading.heading == 45.2
    assert reading.pitch == 2.1
    assert reading.satellite_count == 12
    assert reading.raw_data == {"test": "data"}


def test_position_sensor_reading_invalid_heading():
    """Test that invalid heading is caught by validation."""
    with pytest.raises(ValidationError) as exc_info:
        PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
            heading=400,  # Invalid! Must be 0-360
        )

    assert "heading" in str(exc_info.value)


def test_position_sensor_reading_invalid_pitch():
    """Test that invalid pitch is caught by validation."""
    with pytest.raises(ValidationError):
        PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
            pitch=100,  # Invalid! Must be -90 to 90
        )


def test_position_sensor_reading_invalid_roll():
    """Test that invalid roll is caught by validation."""
    with pytest.raises(ValidationError):
        PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
            roll=200,  # Invalid! Must be -180 to 180
        )


def test_position_sensor_reading_json_serialization():
    """Test that readings can be serialized to JSON."""
    reading = PositionSensorReadingDTO(
        recorded_at=datetime(2025, 12, 7, 19, 0, 0, 123000, tzinfo=timezone.utc),
        x=-122.4194,
        y=37.7749,
        altitude=10.5,
        heading=45.2,
    )

    json_data = reading.model_dump(mode="json", exclude_none=True)

    assert json_data["x"] == -122.4194
    assert json_data["y"] == 37.7749
    assert json_data["altitude"] == 10.5
    assert json_data["heading"] == 45.2
    assert "recorded_at" in json_data


def test_sensor_reading_response():
    """Test sensor reading response DTO."""
    response = SensorReadingResponse(
        message="Reading stored successfully",
        id=123,
    )

    assert response.message == "Reading stored successfully"
    assert response.id == 123
