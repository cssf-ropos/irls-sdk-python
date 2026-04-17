"""Data Transfer Objects for CTD sensor readings."""

from typing import Optional, Dict
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AMLCTDSensorReadingDTO(BaseModel):
    """DTO for CTD sensor readings.

    This DTO represents all data that can be sent to the IRLS CTD sensor API.
    Required fields are date, time, conductivity, temperature_ctd, dissolved_o2,
    temperature_do, and pressure. All other fields are optional.


    Example Sentence:
    2024-11-13,17:56:28.16,29.266,2.328,237.51,2.35,58.91,-0.00,0.00

    Fields:
        0: Date (yyyy-mm-dd)
        1: Time (hh:mm:ss.ss)
        2: Conductivity (mS/cm)
        3: Temperature CTD (C)
        4: Dissolved O2 (umol/l)
        5: Temperature DO (C)
        6: Pressure (dbar)
        7: V1 (Volts)
        8: V2 (Volts)

    Example:
        >>> from datetime import datetime, timezone
        >>> reading = CTDSensorReadingDTO(
        ...     date="2024-11-13",
        ...     time="17:56:28.16",
        ...     conductivity=29.266,
        ...     temperature_ctd=2.328,
        ...     pressure=58.91,
        ...     dissolved_o2=237.51,
        ...     temperature_do=2.35,
        ...     v1=-0.00,
        ...     v2=0.00
        ... )
    """
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"}
    )
    # Required fields
    recorded_at: datetime = Field(
        ..., description="Timestamp when the reading was recorded (ISO 8601 with milliseconds)"
    )
    date: str = Field(..., description="Date when the reading was recorded (yyyy-mm-dd)")
    time: str = Field(..., description="Time when the reading was recorded (hh:mm:ss.ss)")
    conductivity: float = Field(None, ge=0, le=100, description="Conductivity in mS/cm")
    temperature_ctd: float = Field(None, ge=-5, le=40, description="Temperature CTD in C")
    dissolved_o2: float = Field(None, ge=0, le=500, description="Dissolved O2 in umol/l")
    temperature_do: float = Field(None, ge=-5, le=40, description="Temperature DO in C")
    pressure: float = Field(None, ge=0, le=500, description="Pressure in dbar")

    # Optional fields
    v1: Optional[float] = Field(None, description="V1 in Volts")
    v2: Optional[float] = Field(None, description="V2 in Volts")


class AMLCTDSensorReadingResponse(BaseModel):
    """Response from IRLS after successfully storing a sensor reading."""

    message: str = Field(..., description="Success message from IRLS")
    id: int = Field(..., description="ID of the stored reading in IRLS database")
