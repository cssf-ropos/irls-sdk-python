# IRLS Python SDK

Python SDK for CSSF's IRLS 3.0. This SDK provides a clean, type-safe interface for sending sensor data to IRLS, with support for position sensors, scientific sensors, and imaging sensors.

## Features

- 🔒 **Type-safe** - Full type hints with Pydantic DTOs
- ✅ **Validated** - Client-side validation before sending data
- ⚡ **Async support** - Both synchronous and asynchronous clients
- 🎯 **Clean API** - Simple, intuitive interface
- 📝 **Well documented** - Comprehensive examples and docstrings
- 🚀 **Fast** - Built on httpx for high performance

## Installation

### From PyPI (when published)

```bash
# Using pip
pip install irls-sdk

# Using uv
uv add irls-sdk
```

### From GitHub

```bash
# Using pip
pip install git+https://github.com/yourusername/irls-sdk-python.git

# Using uv
uv add git+https://github.com/yourusername/irls-sdk-python.git

# Install a specific branch
uv add git+https://github.com/yourusername/irls-sdk-python.git@branch-name

# Install a specific commit
uv add git+https://github.com/yourusername/irls-sdk-python.git@commit-hash
```

### Local Development

If you're developing the SDK locally and want to use it in another project:

**Using uv (recommended):**

```bash
# In your sensor driver project
cd /path/to/my-sensor-driver
uv add /path/to/irls-sdk-python

# This adds to pyproject.toml:
# [project]
# dependencies = ["irls-sdk"]
#
# [tool.uv.sources]
# irls-sdk = { path = "/path/to/irls-sdk-python" }
```

**Using pip (editable install):**

```bash
# In your sensor driver project
cd /path/to/my-sensor-driver
pip install -e /path/to/irls-sdk-python
```

**Example workflow:**

```bash
# Terminal 1: Working on the SDK
cd ~/code/irls-sdk-python
# Make changes to src/irls/...
# Changes are immediately available to projects using it

# Terminal 2: Using the SDK in your sensor driver
cd ~/code/my-sensor-driver
uv add ~/code/irls-sdk-python

# Create a simple test
cat > test.py << 'EOF'
from irls import IRLSClient
from irls.dto import PositionSensorReadingDTO
from datetime import datetime, timezone

client = IRLSClient(base_url="http://127.0.0.1:8000")
reading = PositionSensorReadingDTO(
    recorded_at=datetime.now(timezone.utc),
    x=-122.4194, y=37.7749, altitude=10.5
)
response = client.position.send(sensor_slug="rovins", data=reading)
print(f"Sent reading ID: {response.id}")
EOF

# Run it
uv run python test.py
```

The local path setup means any changes you make to the SDK are **immediately reflected** in your project without reinstalling!

## Quick Start

```python
from datetime import datetime, timezone
from irls import IRLSClient
from irls.dto import PositionSensorReadingDTO

# Initialize client
client = IRLSClient(base_url="https://your-irls-instance.com")

# Create a reading
reading = PositionSensorReadingDTO(
    recorded_at=datetime.now(timezone.utc),
    x=-122.4194,  # Longitude for WGS84
    y=37.7749,     # Latitude for WGS84
    altitude=10.5,
    satellite_count=12,
    status="GPS_FIX"
)

# Send to IRLS
response = client.position.send(sensor_slug="gps-primary", data=reading)
print(f"Reading stored with ID: {response.id}")
```

## Usage

### Position Sensors

Position sensors include GPS, INS, USBL, and other navigation systems.

#### Minimal Example

```python
from datetime import datetime, timezone
from irls import IRLSClient
from irls.dto import PositionSensorReadingDTO

client = IRLSClient(base_url="https://irls.example.com")

reading = PositionSensorReadingDTO(
    recorded_at=datetime.now(timezone.utc),
    x=-122.4194,
    y=37.7749,
    altitude=10.5
)

response = client.position.send(sensor_slug="rovins", data=reading)
```

#### Full Navigation Data

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
    raw_data={"mode": "RTK_FIXED"}
)

response = client.position.send(sensor_slug="rovins", data=reading)
```

### Async Client

For high-performance applications or when sending many readings concurrently:

```python
import asyncio
from irls import AsyncIRLSClient
from irls.dto import PositionSensorReadingDTO

async def main():
    client = AsyncIRLSClient(base_url="https://irls.example.com")
    
    reading = PositionSensorReadingDTO(
        recorded_at=datetime.now(timezone.utc),
        x=-122.4194,
        y=37.7749,
        altitude=10.5
    )
    
    response = await client.position.send(sensor_slug="rovins", data=reading)
    print(f"Reading ID: {response.id}")

asyncio.run(main())
```

### Error Handling

```python
from irls.exceptions import (
    SensorNotFoundError,
    SensorDisabledError,
    ValidationError,
    RequestError,
)

try:
    response = client.position.send(sensor_slug="my-sensor", data=reading)
except SensorNotFoundError as e:
    print(f"Sensor '{e.sensor_slug}' not found")
except SensorDisabledError as e:
    print(f"Sensor '{e.sensor_slug}' is disabled")
except ValidationError as e:
    print(f"Validation error: {e.errors}")
except RequestError as e:
    print(f"Request failed: {e}")
```

### Configuration

```python
client = IRLSClient(
    base_url="https://irls.example.com",
    timeout=30.0,    # Request timeout in seconds
    verbose=True     # Enable debug logging
)
```

## Coordinate Systems

The SDK supports multiple coordinate reference systems (SRID):

- **WGS84 (SRID 4326)** - Default GPS coordinates
  - `x` = longitude (-180 to 180)
  - `y` = latitude (-90 to 90)
- **UTM Zones** - Universal Transverse Mercator
  - `x` = easting (meters)
  - `y` = northing (meters)
- **Custom Projections** - Any EPSG-defined coordinate system

The sensor's SRID is configured in the IRLS admin interface. Always send coordinates in the format expected by your sensor's configured SRID.

## Field Reference

### PositionSensorReadingDTO

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `recorded_at` | datetime | Timestamp when reading was recorded (UTC) |
| `x` | float | X coordinate (longitude for WGS84, easting for UTM) |
| `y` | float | Y coordinate (latitude for WGS84, northing for UTM) |
| `altitude` | float | Altitude in meters (MSL) |

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
| `altitude_above_ground` | float | ≥ 0 | AGL in meters |
| `course_over_ground` | float | 0-360 | COG in degrees |
| `north_velocity` | float | - | North velocity in m/s |
| `east_velocity` | float | - | East velocity in m/s |
| `position_stddev` | float | ≥ 0 | Position std dev in meters |
| `altitude_stddev` | float | ≥ 0 | Altitude std dev in meters |
| `heading_stddev` | float | ≥ 0 | Heading std dev in degrees |
| `roll_stddev` | float | ≥ 0 | Roll std dev in degrees |
| `pitch_stddev` | float | ≥ 0 | Pitch std dev in degrees |
| `status` | str | max 50 | Sensor status (e.g., "GPS_FIX", "RTK_FIXED") |
| `satellite_count` | int | 0-100 | Number of satellites |
| `hdop` | float | ≥ 0 | Horizontal Dilution of Precision |
| `raw_data` | dict | - | Raw sensor data (JSON object) |

## Examples

See the [`examples/`](examples/) directory for more usage examples:

- [`simple_gps.py`](examples/simple_gps.py) - Basic GPS reading
- [`full_navigation.py`](examples/full_navigation.py) - Complete INS/navigation data
- [`async_example.py`](examples/async_example.py) - Async client usage
- [`error_handling.py`](examples/error_handling.py) - Error handling patterns

## Development

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python dependency management.

### Getting Started

**1. Install uv** (if you don't have it)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

**2. Clone and Setup**

```bash
# Clone the repository
git clone https://github.com/yourusername/irls-sdk-python.git
cd irls-sdk-python

# Install dependencies (creates .venv automatically)
uv sync

# Activate the virtual environment (optional - uv run handles this)
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows
```

**3. Run Examples**

```bash
# Run any example
uv run python examples/simple_gps.py

# Or if you activated the venv
python examples/simple_gps.py
```

### Development Commands

```bash
# Run tests (unit tests don't require IRLS API to be running)
uv run pytest

# Run only unit tests (fast, no API needed)
uv run pytest tests/unit/

# Run integration tests (requires IRLS API running at http://127.0.0.1:8000)
uv run pytest tests/integration/

# Run with coverage
uv run pytest --cov=irls --cov-report=term-missing

# Format code
uv run black src/

# Lint
uv run ruff check src/

# Type check
uv run mypy src/

# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name
```

### Project Structure

```
irls-sdk-python/
├── src/irls/              # Main SDK package
│   ├── dto/               # Data Transfer Objects (DTOs)
│   ├── sensors/           # Sensor-specific clients
│   ├── client.py          # Main IRLSClient and AsyncIRLSClient
│   └── exceptions.py      # Custom exception classes
├── examples/              # Usage examples
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test fixtures
├── pyproject.toml         # Project configuration and dependencies
└── README.md              # This file
```

### Making Changes

1. Create a new branch for your feature
2. Make your changes in `src/irls/`
3. Add tests in `tests/`
4. Run the test suite: `uv run pytest`
5. Format and lint: `uv run black src/ && uv run ruff check src/`
6. Submit a pull request

### Testing Changes in Another Project

If you're developing the SDK and want to test it in another project before publishing:

```bash
# In your sensor driver project
cd /path/to/my-sensor-driver

# Add the local SDK as a dependency
uv add /path/to/irls-sdk-python

# Now you can import and use it
# from irls import IRLSClient
```

Changes to the SDK will be immediately available in your project without reinstalling.

### Testing Against a Local IRLS Instance

The repository includes a manual integration test script:

```bash
# Start your IRLS API (in another terminal)
cd /path/to/irls-3
php artisan serve

# Run the integration test
cd /path/to/irls-sdk-python
uv run python test_local.py
```

This script tests:

- Sending minimal readings
- Sending full readings with all fields
- Error handling (sensor not found, validation errors)
- Client-side validation

**Note**: Unit tests in `tests/unit/` don't require the API running and can be run anytime with `uv run pytest tests/unit/`.

### Building and Publishing

```bash
# Build the package
uv build

# Publish to PyPI (requires credentials)
uv publish

# Or publish to TestPyPI first
uv publish --publish-url https://test.pypi.org/legacy/
```

## Requirements

- Python 3.10+
- pydantic >= 2.0
- httpx >= 0.24

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Future Sensor Types

The SDK is designed to be extended with additional sensor types:

- **Scientific Sensors** - pH meters, temperature sensors, etc.
- **Imaging Sensors** - Cameras, imaging systems

When these endpoints are added to the IRLS API, extending the SDK is straightforward:

1. Add a new DTO in `src/irls/dto/`
2. Add a new client in `src/irls/sensors/`
3. Wire it into the main `IRLSClient`

See the position sensor implementation as a reference.

## Requirements

- Python 3.10+
- pydantic >= 2.0
- httpx >= 0.24

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue on GitHub or contact the maintainers.
