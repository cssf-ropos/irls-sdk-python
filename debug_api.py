#!/usr/bin/env python3
"""Debug script to check IRLS API endpoint."""

import httpx
from datetime import datetime, timezone

# Test the raw endpoint
url = "http://127.0.0.1:8000/api/sensors/position/rovins/data"

payload = {
    "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    "x": -122.4194,
    "y": 37.7749,
    "altitude": 10.5,
}

print(f"Testing URL: {url}")
print(f"Payload: {payload}")
print()

try:
    response = httpx.post(url, json=payload, follow_redirects=False)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Body: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
