"""Data Transfer Objects for position sensor readings."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class PositionSensorReadingDTO(BaseModel):
    """DTO for position sensor readings.

    This DTO represents all data that can be sent to the IRLS position sensor API.
    Only required fields are recorded_at, x, y, and altitude. All other fields are optional.

    Coordinate Systems:
        - For WGS84 (SRID 4326): x=longitude, y=latitude
        - For UTM zones: x=easting, y=northing
        - The sensor's SRID is configured in IRLS admin interface

    Example:
        >>> from datetime import datetime, timezone
        >>> reading = PositionSensorReadingDTO(
        ...     recorded_at=datetime.now(timezone.utc),
        ...     x=-122.4194,  # longitude for WGS84
        ...     y=37.7749,     # latitude for WGS84
        ...     altitude=10.5,
        ...     heading=45.2,
        ...     satellite_count=12,
        ...     status="GPS_FIX"
        ... )
    """

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"}
    )

    # Required fields
    recorded_at: datetime = Field(
        ..., description="Timestamp when the reading was recorded (ISO 8601 with milliseconds)"
    )
    x: float = Field(..., description="X coordinate (longitude for WGS84, easting for UTM)")
    y: float = Field(..., description="Y coordinate (latitude for WGS84, northing for UTM)")
    altitude: float = Field(..., description="Altitude in meters (relative to MSL)")

    # Navigation optional fields
    heading: Optional[float] = Field(
        None, ge=0, le=360, description="Heading in degrees (0=North, clockwise)"
    )
    pitch: Optional[float] = Field(None, ge=-90, le=90, description="Pitch angle in degrees")
    roll: Optional[float] = Field(None, ge=-180, le=180, description="Roll angle in degrees")

    # Speed fields
    speed: Optional[float] = Field(None, ge=0, description="Speed in meters per second")
    vertical_speed: Optional[float] = Field(None, description="Vertical speed in meters per second")
    forward_speed: Optional[float] = Field(None, description="Forward speed in meters per second")
    lateral_speed: Optional[float] = Field(None, description="Lateral speed in meters per second")

    # Additional position fields
    altitude_above_ground: Optional[float] = Field(
        None, ge=0, description="Altitude above ground level in meters"
    )
    course_over_ground: Optional[float] = Field(
        None, ge=0, le=360, description="Course over ground in degrees"
    )
    north_velocity: Optional[float] = Field(None, description="North component of velocity in m/s")
    east_velocity: Optional[float] = Field(None, description="East component of velocity in m/s")

    # Accuracy/quality fields
    position_stddev: Optional[float] = Field(
        None, ge=0, description="Position standard deviation in meters"
    )
    altitude_stddev: Optional[float] = Field(
        None, ge=0, description="Altitude standard deviation in meters"
    )
    heading_stddev: Optional[float] = Field(
        None, ge=0, description="Heading standard deviation in degrees"
    )
    roll_stddev: Optional[float] = Field(
        None, ge=0, description="Roll standard deviation in degrees"
    )
    pitch_stddev: Optional[float] = Field(
        None, ge=0, description="Pitch standard deviation in degrees"
    )

    # Sensor metadata
    status: Optional[str] = Field(
        None,
        max_length=50,
        description="Sensor-specific status string (e.g., 'GPS_FIX', 'RTK_FIXED')",
    )
    satellite_count: Optional[int] = Field(
        None, ge=0, le=100, description="Number of satellites in view/used"
    )
    hdop: Optional[float] = Field(None, ge=0, description="Horizontal Dilution of Precision")
    raw_data: Optional[Dict[str, Any]] = Field(
        None, description="Raw sensor data for debugging (JSON object)"
    )


class SensorReadingResponse(BaseModel):
    """Response from IRLS after successfully storing a sensor reading."""

    message: str = Field(..., description="Success message from IRLS")
    id: int = Field(..., description="ID of the stored reading in IRLS database")
