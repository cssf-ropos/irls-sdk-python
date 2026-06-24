"""Data Transfer Objects for CTD sensor readings."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from irls.dto.common import ScientificUnit


class ExtraMeasurementDTO(BaseModel):
    """A single auxiliary sensor measurement for inclusion in a CTD reading.

    Example:
        >>> m = ExtraMeasurementDTO(name="fluorescence", value=0.18, unit="micrograms_per_litre")
    """

    name: str = Field(..., max_length=100, description="Measurement name (e.g., 'fluorescence')")
    value: float = Field(..., description="Numeric measurement value")
    unit: ScientificUnit = Field(..., description="Scientific unit — must be a valid ScientificUnit value")


class CTDSensorReadingDTO(BaseModel):
    """DTO for CTD (Conductivity, Temperature, Depth) sensor readings.

    Required fields are recorded_at, temperature, conductivity, and pressure.
    All other fields are optional.

    Example:
        >>> from datetime import datetime, timezone
        >>> reading = CTDSensorReadingDTO(
        ...     recorded_at=datetime.now(timezone.utc),
        ...     temperature=4.82,
        ...     conductivity=3.12,
        ...     pressure=512.5,
        ...     salinity=34.89,
        ... )
    """

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"}
    )

    # Required fields
    recorded_at: datetime = Field(
        ..., description="Timestamp when the reading was recorded (ISO 8601 with milliseconds)"
    )
    temperature: float = Field(..., description="Water temperature (°C)")
    conductivity: float = Field(..., description="Electrical conductivity (S/m or mS/cm)")
    pressure: float = Field(..., ge=0, description="Water pressure (dbar)")

    # Standard optional fields
    salinity: Optional[float] = Field(None, ge=0, description="Practical salinity (PSU)")
    dissolved_oxygen: Optional[float] = Field(
        None, ge=0, description="Dissolved oxygen concentration (µmol/L)"
    )
    sound_velocity: Optional[float] = Field(
        None, ge=0, description="Speed of sound in water (m/s)"
    )
    turbidity: Optional[float] = Field(None, ge=0, description="Water turbidity (NTU)")
    density: Optional[float] = Field(None, description="Water density (kg/m³)")
    status: Optional[str] = Field(
        None, max_length=50, description="Sensor-specific status string (e.g., 'OK', 'WARN')"
    )
    raw_data: Optional[Dict[str, Any]] = Field(
        None, description="Raw sensor output for debugging (JSON object)"
    )

    # Auxiliary sensor measurements
    extra_measurements: Optional[List[ExtraMeasurementDTO]] = Field(
        None, description="Custom measurements for auxiliary sensors (fluorescence, PAR, pH, etc.)"
    )
