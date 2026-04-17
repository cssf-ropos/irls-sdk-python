"""Unit tests for DTOs - no API required."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from irls.dto import AMLCTDSensorReadingDTO, AMLCTDSensorReadingResponse


def test_aml_ctd_sensor_reading_minimal():
    """Test creating a minimal AML CTD sensor reading."""
    reading = AMLCTDSensorReadingDTO(
        date="2024-11-13",
        time="17:56:28.16",
        conductivity=29.266,
        temperature_ctd=2.328,
        pressure=58.91,
        dissolved_o2=237.51,
        temperature_do=2.35,
    )

    assert reading.date == "2024-11-13"
    assert reading.time == "17:56:28.16"
    assert reading.conductivity == 29.266
    assert reading.temperature_ctd == 2.328
    assert reading.pressure == 58.91
    assert reading.dissolved_o2 == 237.51
    assert reading.temperature_do == 2.35

def test_aml_ctd_sensor_reading_full():
    """Test creating a full AML CTD sensor reading with all fields."""

    reading = AMLCTDSensorReadingDTO(
        date="2024-11-13",
        time="17:56:28.16",
        conductivity=29.266,
        temperature_ctd=2.328,
        pressure=58.91,
        dissolved_o2=237.51,
        temperature_do=2.35,
        v1=-0.50,
        v2=0.32,
    )

    assert reading.date == "2024-11-13"
    assert reading.time == "17:56:28.16"
    assert reading.conductivity == 29.266
    assert reading.temperature_ctd == 2.328
    assert reading.pressure == 58.91
    assert reading.dissolved_o2 == 237.51
    assert reading.temperature_do == 2.35
    assert reading.v1 == -0.50
    assert reading.v2 == 0.32


def test_aml_ctd_sensor_reading_invalid_conductivity():
    """Test that invalid conductivity is caught by validation."""
    with pytest.raises(ValidationError):
        AMLCTDSensorReadingDTO(
            date="2024-11-13",
            time="17:56:28.16",
            conductivity=-1,  # Invalid! Must be 0-100
            temperature_ctd=2.328,
            pressure=58.91,
            dissolved_o2=237.51,
            temperature_do=2.35,
        )


def test_aml_ctd_sensor_reading_invalid_ctd_temp():
    """Test that invalid CTD temperature is caught by validation."""
    with pytest.raises(ValidationError):
        AMLCTDSensorReadingDTO(
            date="2024-11-13",
            time="17:56:28.16",
            conductivity=29.266,
            temperature_ctd=-10,  # Invalid! Must be -5 to 40
            pressure=58.91,
            dissolved_o2=237.51,
            temperature_do=2.35,
        )

def test_aml_ctd_sensor_reading_invalid_pressure():
    """Test that invalid pressure is caught by validation."""
    with pytest.raises(ValidationError):
        AMLCTDSensorReadingDTO(
            date="2024-11-13",
            time="17:56:28.16",
            conductivity=29.266,
            temperature_ctd=2.328,
            pressure=1000,  # Invalid! Must be 0-100
            dissolved_o2=237.51,
            temperature_do=2.35,
        )

def test_aml_ctd_sensor_reading_invalid_o2():
    """Test that invalid dissolved oxygen is caught by validation."""
    with pytest.raises(ValidationError):
        AMLCTDSensorReadingDTO(
            date="2024-11-13",
            time="17:56:28.16",
            conductivity=29.266,
            temperature_ctd=2.328,
            pressure=58.91,
            dissolved_o2=600,  # Invalid! Must be 0-500
            temperature_do=2.35,
        )


def test_aml_ctd_sensor_reading_invalid_do_temp():
    """Test that invalid DO temperature is caught by validation."""
    with pytest.raises(ValidationError):
        AMLCTDSensorReadingDTO(
            date="2024-11-13",
            time="17:56:28.16",
            conductivity=29.266,
            temperature_ctd=2.328,
            pressure=58.91,
            dissolved_o2=237.51,
            temperature_do=-10,  # Invalid! Must be -5 to 40
        )

def test_aml_ctd_sensor_reading_json_serialization():
    """Test that readings can be serialized to JSON."""
    reading = AMLCTDSensorReadingDTO(
        date="2024-11-13",
        time="17:56:28.16",
        conductivity=29.266,
        temperature_ctd=2.328,
        pressure=58.91,
        dissolved_o2=237.51,
        temperature_do=2.35,
        v1=-0.50,
        v2=0.32,
    )

    json_data = reading.model_dump(mode="json", exclude_none=True)

    assert json_data["date"] == "2024-11-13"
    assert json_data["time"] == "17:56:28.16"
    assert json_data["conductivity"] == 29.266
    assert json_data["temperature_ctd"] == 2.328
    assert json_data["pressure"] == 58.91
    assert json_data["dissolved_o2"] == 237.51
    assert json_data["temperature_do"] == 2.35
    assert json_data["v1"] == -0.50
    assert json_data["v2"] == 0.32


def test_sensor_reading_response():
    """Test sensor reading response DTO."""
    response = AMLCTDSensorReadingResponse(
        message="Reading stored successfully",
        id=123,
    )

    assert response.message == "Reading stored successfully"
    assert response.id == 123
