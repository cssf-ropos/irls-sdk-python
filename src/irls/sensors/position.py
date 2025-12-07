"""Position sensor client for IRLS SDK."""

import logging
from typing import Optional

import httpx

from irls.dto.position import PositionSensorReadingDTO, SensorReadingResponse
from irls.exceptions import (
    APIDisabledError,
    RequestError,
    SensorDisabledError,
    SensorNotFoundError,
    ValidationError,
)

logger = logging.getLogger(__name__)


class PositionSensorClient:
    """Client for interacting with IRLS position sensor API.

    This client handles sending position sensor readings to IRLS.
    It supports synchronous operations using httpx.

    Args:
        base_url: Base URL of the IRLS instance (e.g., "http://127.0.0.1:8000")
        timeout: Request timeout in seconds
        verbose: Enable verbose logging
    """

    def __init__(self, base_url: str, timeout: float = 30.0, verbose: bool = False) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verbose = verbose

        if self.verbose:
            logger.setLevel(logging.DEBUG)
            if not logger.handlers:
                handler = logging.StreamHandler()
                handler.setFormatter(
                    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                )
                logger.addHandler(handler)

    def send(self, sensor_slug: str, data: PositionSensorReadingDTO) -> SensorReadingResponse:
        """Send a position sensor reading to IRLS.

        Args:
            sensor_slug: The sensor slug (e.g., "rovins", "gps-primary")
            data: The position sensor reading data

        Returns:
            SensorReadingResponse with the stored reading ID

        Raises:
            SensorNotFoundError: If the sensor slug doesn't exist
            SensorDisabledError: If the sensor is disabled
            APIDisabledError: If the IRLS API is disabled
            ValidationError: If the data validation fails
            RequestError: If the request fails for other reasons

        Example:
            >>> from datetime import datetime, timezone
            >>> from irls.dto import PositionSensorReadingDTO
            >>>
            >>> client = PositionSensorClient(base_url="http://127.0.0.1:8000")
            >>> reading = PositionSensorReadingDTO(
            ...     recorded_at=datetime.now(timezone.utc),
            ...     x=-122.4194,
            ...     y=37.7749,
            ...     altitude=10.5,
            ...     heading=45.2
            ... )
            >>> response = client.send(sensor_slug="rovins", data=reading)
            >>> print(f"Stored reading ID: {response.id}")
        """
        url = f"{self.base_url}/api/sensors/position/{sensor_slug}/data"

        # Convert DTO to JSON dict
        payload = data.model_dump(mode="json", exclude_none=True)

        if self.verbose:
            logger.debug(f"Sending position reading to {url}")
            logger.debug(f"Payload: {payload}")

        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                response = client.post(url, json=payload, headers=headers)

                if self.verbose:
                    logger.debug(f"Response status: {response.status_code}")
                    logger.debug(f"Response body: {response.text}")

                # Handle different error cases
                if response.status_code == 404:
                    # Could be sensor not found or API disabled
                    try:
                        error_data = response.json()
                        message = error_data.get("message", "")
                        if "No query results" in message or sensor_slug in message:
                            raise SensorNotFoundError(sensor_slug, message)
                        else:
                            raise APIDisabledError(message)
                    except (ValueError, KeyError):
                        # If we can't parse JSON, assume API disabled
                        raise APIDisabledError()

                elif response.status_code == 403:
                    error_data = response.json()
                    message = error_data.get("message", "Sensor is disabled")
                    raise SensorDisabledError(sensor_slug, message)

                elif response.status_code == 422:
                    error_data = response.json()
                    message = error_data.get("message", "Validation failed")
                    errors = error_data.get("errors", {})
                    raise ValidationError(message, errors)

                elif response.status_code != 201:
                    raise RequestError(
                        f"Request failed: {response.text}",
                        status_code=response.status_code,
                        response_text=response.text,
                    )

                # Success - parse response
                response_data = response.json()
                return SensorReadingResponse(**response_data)

        except httpx.TimeoutException as e:
            raise RequestError(f"Request timed out after {self.timeout}s") from e
        except httpx.RequestError as e:
            raise RequestError(f"Request failed: {str(e)}") from e


class AsyncPositionSensorClient:
    """Async client for interacting with IRLS position sensor API.

    This client provides async operations for high-performance applications.

    Args:
        base_url: Base URL of the IRLS instance (e.g., "http://127.0.0.1:8000")
        timeout: Request timeout in seconds
        verbose: Enable verbose logging
    """

    def __init__(self, base_url: str, timeout: float = 30.0, verbose: bool = False) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verbose = verbose

        if self.verbose:
            logger.setLevel(logging.DEBUG)
            if not logger.handlers:
                handler = logging.StreamHandler()
                handler.setFormatter(
                    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                )
                logger.addHandler(handler)

    async def send(self, sensor_slug: str, data: PositionSensorReadingDTO) -> SensorReadingResponse:
        """Send a position sensor reading to IRLS asynchronously.

        Args:
            sensor_slug: The sensor slug (e.g., "rovins", "gps-primary")
            data: The position sensor reading data

        Returns:
            SensorReadingResponse with the stored reading ID

        Raises:
            SensorNotFoundError: If the sensor slug doesn't exist
            SensorDisabledError: If the sensor is disabled
            APIDisabledError: If the IRLS API is disabled
            ValidationError: If the data validation fails
            RequestError: If the request fails for other reasons

        Example:
            >>> import asyncio
            >>> from datetime import datetime, timezone
            >>> from irls.dto import PositionSensorReadingDTO
            >>>
            >>> async def main():
            ...     client = AsyncPositionSensorClient(base_url="http://127.0.0.1:8000")
            ...     reading = PositionSensorReadingDTO(
            ...         recorded_at=datetime.now(timezone.utc),
            ...         x=-122.4194,
            ...         y=37.7749,
            ...         altitude=10.5
            ...     )
            ...     response = await client.send(sensor_slug="rovins", data=reading)
            ...     print(f"Stored reading ID: {response.id}")
            >>>
            >>> asyncio.run(main())
        """
        url = f"{self.base_url}/api/sensors/position/{sensor_slug}/data"

        # Convert DTO to JSON dict
        payload = data.model_dump(mode="json", exclude_none=True)

        if self.verbose:
            logger.debug(f"Sending position reading to {url}")
            logger.debug(f"Payload: {payload}")

        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.post(url, json=payload, headers=headers)

                if self.verbose:
                    logger.debug(f"Response status: {response.status_code}")
                    logger.debug(f"Response body: {response.text}")

                # Handle different error cases
                if response.status_code == 404:
                    try:
                        error_data = response.json()
                        message = error_data.get("message", "")
                        if "No query results" in message or sensor_slug in message:
                            raise SensorNotFoundError(sensor_slug, message)
                        else:
                            raise APIDisabledError(message)
                    except (ValueError, KeyError):
                        raise APIDisabledError()

                elif response.status_code == 403:
                    error_data = response.json()
                    message = error_data.get("message", "Sensor is disabled")
                    raise SensorDisabledError(sensor_slug, message)

                elif response.status_code == 422:
                    error_data = response.json()
                    message = error_data.get("message", "Validation failed")
                    errors = error_data.get("errors", {})
                    raise ValidationError(message, errors)

                elif response.status_code != 201:
                    raise RequestError(
                        f"Request failed: {response.text}",
                        status_code=response.status_code,
                        response_text=response.text,
                    )

                # Success - parse response
                response_data = response.json()
                return SensorReadingResponse(**response_data)

        except httpx.TimeoutException as e:
            raise RequestError(f"Request timed out after {self.timeout}s") from e
        except httpx.RequestError as e:
            raise RequestError(f"Request failed: {str(e)}") from e
