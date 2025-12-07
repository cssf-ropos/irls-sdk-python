#!/usr/bin/env python3
"""Example: Send full INS/navigation data to IRLS."""

from datetime import datetime, timezone

from irls import IRLSClient
from irls.dto import PositionSensorReadingDTO

# Initialize client
client = IRLSClient(base_url="http://127.0.0.1:8000")

# Create a full INS reading with all navigation data
reading = PositionSensorReadingDTO(
    recorded_at=datetime.now(timezone.utc),
    x=-122.4194,
    y=37.7749,
    altitude=10.5,
    # Orientation
    heading=45.2,
    pitch=2.1,
    roll=-1.5,
    # Speed
    speed=5.3,
    vertical_speed=0.1,
    forward_speed=5.2,
    lateral_speed=0.3,
    # Additional position data
    altitude_above_ground=8.2,
    course_over_ground=46.1,
    north_velocity=3.7,
    east_velocity=3.8,
    # Accuracy metrics
    position_stddev=0.5,
    altitude_stddev=0.3,
    heading_stddev=0.2,
    roll_stddev=0.1,
    pitch_stddev=0.1,
    # GPS quality
    status="INS_NAVIGATION",
    satellite_count=12,
    hdop=1.2,
    # Raw sensor data for debugging
    raw_data={
        "sentence": "$GPGGA,142345.123,3746.494,N,12225.164,W,1,12,1.2,10.5,M,0.0,M,,*6E",
        "mode": "RTK_FIXED",
    },
)

# Send to IRLS
response = client.position.send(sensor_slug="rovins", data=reading)

print(f"✓ {response.message}")
print(f"✓ Reading ID: {response.id}")
