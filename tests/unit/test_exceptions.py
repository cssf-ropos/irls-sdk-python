"""Unit tests for exceptions - no API required."""

from irls.exceptions import (
    APIDisabledError,
    IRLSError,
    RequestError,
    SensorDisabledError,
    SensorNotFoundError,
    ValidationError,
)


def test_sensor_not_found_error():
    """Test SensorNotFoundError."""
    error = SensorNotFoundError(sensor_slug="test-sensor")

    assert error.sensor_slug == "test-sensor"
    assert "test-sensor" in str(error)
    assert isinstance(error, IRLSError)


def test_sensor_not_found_error_custom_message():
    """Test SensorNotFoundError with custom message."""
    error = SensorNotFoundError(sensor_slug="test", message="Custom error")

    assert error.message == "Custom error"
    assert str(error) == "Custom error"


def test_sensor_disabled_error():
    """Test SensorDisabledError."""
    error = SensorDisabledError(sensor_slug="disabled-sensor")

    assert error.sensor_slug == "disabled-sensor"
    assert "disabled-sensor" in str(error)


def test_api_disabled_error():
    """Test APIDisabledError."""
    error = APIDisabledError()

    assert "disabled" in str(error).lower()


def test_validation_error():
    """Test ValidationError."""
    errors = {
        "x": ["The x field is required."],
        "y": ["The y field is required."],
    }
    error = ValidationError(message="Validation failed", errors=errors)

    assert error.message == "Validation failed"
    assert error.errors == errors
    assert "x" in str(error)
    assert "y" in str(error)


def test_validation_error_without_errors():
    """Test ValidationError without errors dict."""
    error = ValidationError(message="Validation failed")

    assert error.errors == {}
    assert str(error) == "Validation failed"


def test_request_error():
    """Test RequestError."""
    error = RequestError(
        message="Connection failed",
        status_code=500,
        response_text="Internal Server Error",
    )

    assert error.status_code == 500
    assert error.response_text == "Internal Server Error"
    assert "500" in str(error)


def test_request_error_without_status():
    """Test RequestError without status code."""
    error = RequestError(message="Connection timeout")

    assert error.status_code is None
    assert str(error) == "Connection timeout"
