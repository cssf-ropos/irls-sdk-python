#!/usr/bin/env python3
"""Example: Proper error handling."""

from datetime import datetime, timezone

from irls import IRLSClient
from irls.dto import PositionSensorReadingDTO
from irls.exceptions import (
    SensorDisabledError,
    SensorNotFoundError,
    ValidationError,
    RequestError,
)


def main() -> None:
    """Demonstrate error handling."""
    client = IRLSClient(base_url="http://127.0.0.1:8000")

    # Example 1: Sensor not found
    print("Example 1: Handling sensor not found...")
    try:
        reading = PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
        )
        client.position.send(sensor_slug="nonexistent", data=reading)
    except SensorNotFoundError as e:
        print(f"  ✗ Error: {e}")
        print(f"  → Sensor slug: {e.sensor_slug}")

    # Example 2: Sensor disabled
    print("\nExample 2: Handling disabled sensor...")
    try:
        reading = PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
        )
        # This would fail if sensor was disabled
        # client.position.send(sensor_slug="disabled-sensor", data=reading)
        print("  → (Skipped - no disabled sensor to test)")
    except SensorDisabledError as e:
        print(f"  ✗ Error: {e}")

    # Example 3: Validation error (caught by Pydantic before sending)
    print("\nExample 3: Client-side validation...")
    try:
        reading = PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
            heading=400,  # Invalid! Must be 0-360
        )
    except Exception as e:
        print(f"  ✗ Pydantic validation error: Invalid heading value")

    # Example 4: Server-side validation error
    print("\nExample 4: Handling server validation errors...")
    try:
        # Note: This would only happen if server validation differs from client
        reading = PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
        )
        # Hypothetical server-side validation error
        print("  → (No server validation errors in this example)")
    except ValidationError as e:
        print(f"  ✗ Server validation error: {e}")
        print(f"  → Errors: {e.errors}")

    # Example 5: Network errors
    print("\nExample 5: Handling network errors...")
    try:
        bad_client = IRLSClient(base_url="http://localhost:9999", timeout=1.0)
        reading = PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
        )
        bad_client.position.send(sensor_slug="rovins", data=reading)
    except RequestError as e:
        print(f"  ✗ Network error: Connection failed")


if __name__ == "__main__":
    main()
