#!/usr/bin/env python3
"""Example: Async client for high-performance applications."""

import asyncio
from datetime import datetime, timezone

from irls import AsyncIRLSClient
from irls.dto import PositionSensorReadingDTO


async def send_reading(client: AsyncIRLSClient, sensor_slug: str, index: int) -> None:
    """Send a single reading asynchronously."""
    reading = PositionSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        x=-122.4194 + (index * 0.0001),  # Slightly different positions
        y=37.7749 + (index * 0.0001),
        altitude=10.5 + index,
    )

    response = await client.position.send(sensor_slug=sensor_slug, data=reading)
    print(f"✓ Sent reading {index}: ID {response.id}")


async def main() -> None:
    """Send multiple readings concurrently."""
    client = AsyncIRLSClient(base_url="http://127.0.0.1:8000")

    # Send 10 readings concurrently
    tasks = [send_reading(client, "rovins", i) for i in range(10)]

    await asyncio.gather(*tasks)
    print("\n✓ All readings sent successfully!")


if __name__ == "__main__":
    asyncio.run(main())
