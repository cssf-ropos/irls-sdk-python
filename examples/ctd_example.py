"""CTD sensor example for IRLS SDK."""

import asyncio
from datetime import datetime, timezone

from irls import AsyncIRLSClient, IRLSClient
from irls.dto import CTDSensorReadingDTO, ExtraMeasurementDTO

BASE_URL = "http://127.0.0.1:8000"
SENSOR_SLUG = "sbe-911-starboard"


def sync_example():
    client = IRLSClient(base_url=BASE_URL, verbose=True)

    # Minimal reading
    reading = CTDSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        temperature=4.82,
        conductivity=3.12,
        pressure=512.5,
    )
    response = client.ctd.send(sensor_slug=SENSOR_SLUG, data=reading)
    print(f"Stored reading ID: {response.id}")

    # Full reading with auxiliary sensors
    full_reading = CTDSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        temperature=4.82,
        conductivity=3.12,
        pressure=512.5,
        salinity=34.89,
        dissolved_oxygen=298.4,
        sound_velocity=1490.3,
        turbidity=0.21,
        density=1027.6,
        status="OK",
        raw_data={"firmware": "3.2.5", "message_id": 48291},
        extra_measurements=[
            ExtraMeasurementDTO(name="fluorescence", value=0.18, unit="micrograms_per_litre"),
            ExtraMeasurementDTO(name="par", value=0.4, unit="micromol_photons_per_m2_per_s"),
            ExtraMeasurementDTO(name="ph", value=7.92, unit="ph"),
        ],
    )
    response = client.ctd.send(sensor_slug=SENSOR_SLUG, data=full_reading)
    print(f"Stored full reading ID: {response.id}")


async def async_example():
    client = AsyncIRLSClient(base_url=BASE_URL, verbose=True)

    reading = CTDSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        temperature=4.82,
        conductivity=3.12,
        pressure=512.5,
        salinity=34.89,
    )
    response = await client.ctd.send(sensor_slug=SENSOR_SLUG, data=reading)
    print(f"Async stored reading ID: {response.id}")


if __name__ == "__main__":
    sync_example()
    asyncio.run(async_example())
