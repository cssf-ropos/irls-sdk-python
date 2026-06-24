"""IRLS SDK - Python SDK for IRLS 3.0 logging service."""

from irls.client import AsyncIRLSClient, IRLSClient
from irls.dto import CTDSensorReadingDTO, ExtraMeasurementDTO, PositionSensorReadingDTO, SensorReadingResponse, ScientificUnit
from irls.exceptions import (
    APIDisabledError,
    IRLSError,
    RequestError,
    SensorDisabledError,
    SensorNotFoundError,
    ValidationError,
)

__version__ = "0.1.0"

__all__ = [
    # Main clients
    "IRLSClient",
    "AsyncIRLSClient",
    # DTOs
    "PositionSensorReadingDTO",
    "SensorReadingResponse",
    "CTDSensorReadingDTO",
    "ExtraMeasurementDTO",
    "ScientificUnit",
    # Exceptions
    "IRLSError",
    "SensorNotFoundError",
    "SensorDisabledError",
    "APIDisabledError",
    "ValidationError",
    "RequestError",
]
