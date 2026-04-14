#!/usr/bin/env python3
"""Simple example: Send GPS position data to IRLS."""

from datetime import datetime, timezone

from irls import IRLSClient
from irls.dto import AMLCTDSensorReadingDTO

# Initialize the IRLS client with verbose logging
client = IRLSClient(base_url="http://127.0.0.1:8000", verbose=True)

# Create an AML CTD reading
reading = AMLCTDSensorReadingDTO(
    date="2024-11-13",
    time="14:40:38.17",
    conductivity=27.993,
    temperature_ctd=1.075,
    dissolved_o2=463.55,
    temperature_do=1.12,
    pressure=25.54,
)

# Send to IRLS
response = client.amlctd.send(sensor_slug="aml-ctd", data=reading)

print(f"✓ {response.message}")
print(f"✓ Reading ID: {response.id}")
