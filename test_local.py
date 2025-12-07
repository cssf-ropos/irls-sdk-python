#!/usr/bin/env python3
"""Test script for local IRLS API at http://127.0.0.1:8000"""

from datetime import datetime, timezone

from irls import IRLSClient
from irls.dto import PositionSensorReadingDTO
from irls.exceptions import (
    SensorDisabledError,
    SensorNotFoundError,
    ValidationError,
)


def main() -> None:
    """Test the SDK against local IRLS API."""

    # Initialize client with verbose mode to see what's happening
    client = IRLSClient(base_url="http://127.0.0.1:8000", timeout=10.0, verbose=True)

    print("=" * 60)
    print("Testing IRLS SDK against local API")
    print("=" * 60)

    # Test 1: Send a minimal reading
    print("\n[Test 1] Sending minimal position reading to 'rovins'...")
    try:
        reading = PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,  # longitude
            y=37.7749,  # latitude
            altitude=10.5,
        )

        response = client.position.send(sensor_slug="rovins", data=reading)
        print(f"✓ Success! {response.message}")
        print(f"✓ Reading ID: {response.id}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 2: Send a full reading with all optional fields
    print("\n[Test 2] Sending full position reading with all fields...")
    try:
        reading = PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
            heading=45.2,
            pitch=2.1,
            roll=-1.5,
            speed=5.3,
            vertical_speed=0.1,
            forward_speed=5.2,
            lateral_speed=0.3,
            altitude_above_ground=8.2,
            course_over_ground=46.1,
            north_velocity=3.7,
            east_velocity=3.8,
            position_stddev=0.5,
            altitude_stddev=0.3,
            heading_stddev=0.2,
            roll_stddev=0.1,
            pitch_stddev=0.1,
            status="GPS_FIX",
            satellite_count=12,
            hdop=1.2,
            raw_data={"nmea": "$GPGGA,...", "mode": "RTK_FIXED"},
        )

        response = client.position.send(sensor_slug="rovins", data=reading)
        print(f"✓ Success! {response.message}")
        print(f"✓ Reading ID: {response.id}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 3: Test validation error (invalid heading)
    print("\n[Test 3] Testing validation error (heading > 360)...")
    try:
        reading = PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
            heading=400,  # Invalid!
        )

        response = client.position.send(sensor_slug="rovins", data=reading)
        print(f"✗ Should have failed validation!")
    except ValidationError as e:
        print(f"✓ Correctly caught validation error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

    # Test 4: Test sensor not found
    print("\n[Test 4] Testing sensor not found error...")
    try:
        reading = PositionSensorReadingDTO(
            recorded_at=datetime.now(timezone.utc),
            x=-122.4194,
            y=37.7749,
            altitude=10.5,
        )

        response = client.position.send(sensor_slug="nonexistent-sensor", data=reading)
        print(f"✗ Should have failed with sensor not found!")
    except SensorNotFoundError as e:
        print(f"✓ Correctly caught sensor not found: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

    print("\n" + "=" * 60)
    print("Tests complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
