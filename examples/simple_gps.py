#!/usr/bin/env python3
"""Simple example: Send GPS position data to IRLS."""

from datetime import datetime, timezone

from irls import IRLSClient
from irls.dto import PositionSensorReadingDTO

# Initialize the IRLS client
client = IRLSClient(base_url="http://127.0.0.1:8000")

# Create a GPS reading
reading = PositionSensorReadingDTO(
    recorded_at=datetime.now(timezone.utc),
    x=-122.4194,  # Longitude (WGS84)
    y=37.7749,  # Latitude (WGS84)
    altitude=10.5,
    satellite_count=12,
    hdop=1.2,
    status="GPS_FIX",
)

# Send to IRLS
response = client.position.send(sensor_slug="rovins", data=reading)

print(f"✓ {response.message}")
print(f"✓ Reading ID: {response.id}")
