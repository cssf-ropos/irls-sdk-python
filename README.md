# IRLS Python SDK

Python SDK for CSSF's IRLS 3.0. It provides a type-safe client for sending sensor data to
IRLS: one client per IRLS sensor type, currently **position** and **CTD**.

The SDK speaks the IRLS API, not any one instrument's format: it has no device names in it.
Parsing a particular device's output (a PHINS, an NMEA GPS, an AML CTD) belongs in a driver
such as [irls3-driver](https://github.com/cssf-ropos/irls3-driver).

## Features

- **Type-safe**: full type hints with Pydantic DTOs
- **Validated**: client-side validation before sending data
- **Sync and async**: `IRLSClient` and `AsyncIRLSClient`
- **Built on httpx**

## Installation

Requires Python 3.11+.

```bash
# Using uv
uv add git+https://github.com/cssf-ropos/irls-sdk-python.git

# Using pip
pip install git+https://github.com/cssf-ropos/irls-sdk-python.git

# A specific branch or commit
uv add git+https://github.com/cssf-ropos/irls-sdk-python.git@branch-or-commit
```

To use a local checkout from another project (changes apply without reinstalling):

```bash
cd /path/to/my-sensor-driver
uv add --editable /path/to/irls-sdk-python   # or: pip install -e /path/to/irls-sdk-python
```

## Quick Start

```python
from datetime import datetime, timezone
from irls import IRLSClient
from irls.dto import PositionSensorReadingDTO

client = IRLSClient(base_url="http://localhost:8000")

reading = PositionSensorReadingDTO(
    recorded_at=datetime.now(timezone.utc),
    x=-122.4194,  # Longitude for WGS84
    y=37.7749,    # Latitude for WGS84
    altitude=10.5,
)

response = client.position.send(sensor_slug="rovins", data=reading)
print(f"Reading stored with ID: {response.id}")
```

## Usage

### Position Sensors

Position sensors include GPS, INS, USBL and other navigation systems. Only `recorded_at`,
`x`, `y` and `altitude` are required; everything else is optional:

```python
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
    # Additional position
    altitude_above_ground=8.2,
    course_over_ground=46.1,
    north_velocity=3.7,
    east_velocity=3.8,
    # Accuracy
    position_stddev=0.5,
    altitude_stddev=0.3,
    heading_stddev=0.2,
    # GPS quality
    satellite_count=12,
    hdop=1.2,
    status="INS_NAVIGATION",
    # Raw data for debugging
    raw_data={"mode": "RTK_FIXED"},
)

response = client.position.send(sensor_slug="rovins", data=reading)
```

### CTD Sensors

Only `recorded_at`, `temperature`, `conductivity` and `pressure` are required. Anything a
device measures beyond the standard fields goes in `extra_measurements`:

```python
from irls.dto import CTDSensorReadingDTO, ExtraMeasurementDTO

reading = CTDSensorReadingDTO(
    recorded_at=datetime.now(timezone.utc),
    temperature=4.82,
    conductivity=3.12,
    pressure=512.5,
    salinity=34.89,
    extra_measurements=[
        ExtraMeasurementDTO(name="fluorescence", value=0.18, unit="micrograms_per_litre"),
        ExtraMeasurementDTO(name="ph", value=7.92, unit="ph"),
    ],
)

response = client.ctd.send(sensor_slug="ctd", data=reading)
```

An extra measurement's `unit` must be one of the `ScientificUnit` values (`from irls.dto import ScientificUnit`).

### Async Client

For sending many readings concurrently:

```python
import asyncio
from datetime import datetime, timezone
from irls import AsyncIRLSClient
from irls.dto import PositionSensorReadingDTO

async def main():
    client = AsyncIRLSClient(base_url="http://localhost:8000")

    reading = PositionSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        x=-122.4194,
        y=37.7749,
        altitude=10.5,
    )

    response = await client.position.send(sensor_slug="rovins", data=reading)
    print(f"Reading ID: {response.id}")

asyncio.run(main())
```

### Error Handling

```python
from irls.exceptions import (
    APIDisabledError,
    RequestError,
    SensorDisabledError,
    SensorNotFoundError,
    ValidationError,
)

try:
    response = client.position.send(sensor_slug="my-sensor", data=reading)
except SensorNotFoundError as e:
    print(f"Sensor '{e.sensor_slug}' not found")
except SensorDisabledError as e:
    print(f"Sensor '{e.sensor_slug}' is disabled")
except APIDisabledError:
    print("The IRLS API is turned off (archive mode)")
except ValidationError as e:
    print(f"Validation error: {e.errors}")
except RequestError as e:
    print(f"Request failed: {e}")
```

All of these inherit from `IRLSError`.

### Configuration

```python
client = IRLSClient(
    base_url="http://localhost:8000",
    timeout=30.0,    # Request timeout in seconds
    verbose=True,    # Enable debug logging
)
```

## Coordinate Systems

Position readings are sent in the coordinate system configured on the sensor in IRLS
(its SRID); IRLS converts them to WGS84 for storage.

- **WGS84 (SRID 4326)**: `x` = longitude (-180 to 180), `y` = latitude (-90 to 90)
- **UTM zones**: `x` = easting (metres), `y` = northing (metres)
- **Other projections**: any EPSG-defined coordinate system

## Field Reference

### PositionSensorReadingDTO

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `recorded_at` | datetime | Timestamp when reading was recorded (UTC) |
| `x` | float | X coordinate (longitude for WGS84, easting for UTM) |
| `y` | float | Y coordinate (latitude for WGS84, northing for UTM) |
| `altitude` | float | Altitude in metres (MSL) |

#### Optional Fields

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `heading` | float | 0-360 | Heading in degrees (0=North, clockwise) |
| `pitch` | float | -90 to 90 | Pitch angle in degrees |
| `roll` | float | -180 to 180 | Roll angle in degrees |
| `speed` | float | ≥ 0 | Speed in m/s |
| `vertical_speed` | float | - | Vertical speed in m/s |
| `forward_speed` | float | - | Forward speed in m/s |
| `lateral_speed` | float | - | Lateral speed in m/s |
| `altitude_above_ground` | float | ≥ 0 | AGL in metres |
| `course_over_ground` | float | 0-360 | COG in degrees |
| `north_velocity` | float | - | North velocity in m/s |
| `east_velocity` | float | - | East velocity in m/s |
| `position_stddev` | float | ≥ 0 | Position std dev in metres |
| `altitude_stddev` | float | ≥ 0 | Altitude std dev in metres |
| `heading_stddev` | float | ≥ 0 | Heading std dev in degrees |
| `roll_stddev` | float | ≥ 0 | Roll std dev in degrees |
| `pitch_stddev` | float | ≥ 0 | Pitch std dev in degrees |
| `status` | str | max 50 | Sensor status (e.g., "GPS_FIX", "RTK_FIXED") |
| `satellite_count` | int | 0-100 | Number of satellites |
| `hdop` | float | ≥ 0 | Horizontal Dilution of Precision |
| `raw_data` | dict | - | Raw sensor data (JSON object) |

### CTDSensorReadingDTO

#### Required Fields

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `recorded_at` | datetime | - | Timestamp when reading was recorded (UTC) |
| `temperature` | float | - | Water temperature (°C) |
| `conductivity` | float | - | Electrical conductivity (S/m or mS/cm) |
| `pressure` | float | ≥ 0 | Water pressure (dbar) |

#### Optional Fields

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `salinity` | float | ≥ 0 | Practical salinity (PSU) |
| `dissolved_oxygen` | float | ≥ 0 | Dissolved oxygen (µmol/L) |
| `sound_velocity` | float | ≥ 0 | Speed of sound in water (m/s) |
| `turbidity` | float | ≥ 0 | Turbidity (NTU) |
| `density` | float | - | Water density (kg/m³) |
| `status` | str | max 50 | Sensor status (e.g., "OK", "WARN") |
| `raw_data` | dict | - | Raw sensor data (JSON object) |
| `extra_measurements` | list[ExtraMeasurementDTO] | - | Other measurements: `name` (max 100), `value`, `unit` (a `ScientificUnit`) |

## Examples

See [`examples/`](examples/):

- [`simple_gps.py`](examples/simple_gps.py): basic GPS reading
- [`full_navigation.py`](examples/full_navigation.py): complete INS/navigation data
- [`ctd_example.py`](examples/ctd_example.py): CTD readings, with extra measurements
- [`async_example.py`](examples/async_example.py): async client usage
- [`error_handling.py`](examples/error_handling.py): error handling patterns

Run one with `uv run python examples/simple_gps.py`.

## Development

This project uses [uv](https://docs.astral.sh/uv/).

```bash
git clone git@github.com:cssf-ropos/irls-sdk-python.git
cd irls-sdk-python
uv sync
```

### Development Commands

```bash
uv run pytest                    # Unit tests; integration tests skip without IRLS_URL
uv run pytest --cov=irls --cov-report=term-missing
uv run black src/ tests/         # Format
uv run ruff check src/ tests/    # Lint
uv run mypy src/                 # Type check
```

### Testing Against a Local IRLS

The integration tests in `tests/integration/` run against a live IRLS when `IRLS_URL` is
set. The target needs the sensors from irls-3's `LocalSensorSeeder` (which
`php artisan migrate --seed` includes):

```bash
IRLS_URL=http://localhost:8000 uv run pytest tests/integration/
```

`test_local.py` is a manual script that sends readings to `http://127.0.0.1:8000` and
prints the results: `uv run python test_local.py`.

To test the SDK, the driver and IRLS together, use `bin/test e2e` in
[irls-home](https://github.com/cssf-ropos/irls-home).

### Project Structure

```
irls-sdk-python/
├── src/irls/              # SDK package
│   ├── dto/               # Data Transfer Objects (DTOs)
│   ├── sensors/           # One client per sensor type
│   ├── client.py          # IRLSClient and AsyncIRLSClient
│   └── exceptions.py      # Exception classes
├── examples/              # Usage examples
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Tests against a live IRLS
│   └── fixtures/          # Test fixtures
└── pyproject.toml
```

### Adding a Sensor Type

The SDK mirrors the IRLS API, so a new sensor type starts with a new endpoint in irls-3.
IRLS only adds one when a sensor type doesn't fit an existing endpoint; a new device of an
existing type needs a driver change, not an SDK change. To add one:

1. Add a DTO in `src/irls/dto/`
2. Add sync and async clients in `src/irls/sensors/`
3. Wire them into `IRLSClient` and `AsyncIRLSClient`

The CTD implementation is a recent, complete reference.

## Contributing

Open an issue or a pull request. This repo is public: never commit internal hostnames,
credentials or ship data.
