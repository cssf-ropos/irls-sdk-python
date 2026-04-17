"""CTD sensor client for IRLS SDK."""

import logging

import httpx

from irls.dto.aml_ctd import AMLCTDSensorReadingDTO, AMLCTDSensorReadingResponse
from irls.exceptions import (
    APIDisabledError,
    RequestError,
    SensorDisabledError,
    SensorNotFoundError,
    ValidationError,
)

logger = logging.getLogger(__name__)


class AMLCTDSensorClient:
    """Client for interacting with IRLS AML CTD sensor API.

    This client handles sending AML CTD sensor readings to IRLS.
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

    def send(self, sensor_slug: str, data: AMLCTDSensorReadingDTO) -> AMLCTDSensorReadingResponse:
        """Send an AML CTD sensor reading to IRLS.

        Args:
            sensor_slug: The sensor slug (e.g., "aml-ctd")
            data: The AML CTD sensor reading data

        Returns:
            AMLCTDSensorReadingResponse with the stored reading ID

        Raises:
            SensorNotFoundError: If the sensor slug doesn't exist
            SensorDisabledError: If the sensor is disabled
            APIDisabledError: If the IRLS API is disabled
            ValidationError: If the data validation fails
            RequestError: If the request fails for other reasons

        Example:
            >>> from datetime import datetime, timezone
            >>> from irls.dto import AMLCTDSensorReadingDTO
            >>>
            >>> client = AMLCTDSensorClient(base_url="http://127.0.0.1:8000")
            >>> reading = AMLCTDSensorReadingDTO(
            ...     recorded_at=datetime.now(timezone.utc),
            ...     date="2024-11-13",
            ...     time="14:40:38.17",
            ...     conductivity=0.000,
            ...     temperature_ctd=1.075,
            ...     dissolved_o2=463.55,
            ...     temp_do=1.12,
            ...     pressure=0.54,
            ... )
            >>> response = client.send(sensor_slug="aml-ctd", data=reading)
            >>> print(f"Stored reading ID: {response.id}")
        """
        url = f"{self.base_url}/api/sensors/ctd/{sensor_slug}/data"

        # Convert DTO to JSON dict
        payload = data.model_dump(mode="json", exclude_none=True)

        if self.verbose:
            logger.debug(f"Sending AML CTD reading to {url}")
            logger.debug(f"DTO recorded_at: {data.recorded_at}")
            logger.debug(f"Full Payload: {payload}")

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
                return AMLCTDSensorReadingResponse(**response_data)

        except httpx.TimeoutException as e:
            raise RequestError(f"Request timed out after {self.timeout}s") from e
        except httpx.RequestError as e:
            raise RequestError(f"Request failed: {str(e)}") from e


class AsyncAMLCTDSensorClient:
    """Async client for interacting with IRLS AML CTD sensor API.

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

    async def send(
        self, sensor_slug: str, data: AMLCTDSensorReadingDTO
    ) -> AMLCTDSensorReadingResponse:
        """Send an AML CTD sensor reading to IRLS asynchronously.

        Args:
            sensor_slug: The sensor slug (e.g., "aml-ctd")
            data: The AML CTD sensor reading data

        Returns:
            AMLCTDSensorReadingResponse with the stored reading ID

        Raises:
            SensorNotFoundError: If the sensor slug doesn't exist
            SensorDisabledError: If the sensor is disabled
            APIDisabledError: If the IRLS API is disabled
            ValidationError: If the data validation fails
            RequestError: If the request fails for other reasons

        Example:
            >>> import asyncio
            >>> from datetime import datetime, timezone
            >>> from irls.dto import AMLCTDSensorReadingDTO
            >>>
            >>> async def main():
            ...     client = AsyncAMLCTDSensorClient(base_url="http://127.0.0.1:8000")
            ...     reading = AMLCTDSensorReadingDTO(
            ...         recorded_at=datetime.now(timezone.utc),
            ...         date="2024-11-13",
            ...         time="14:40:38.17",
            ...         conductivity=0.000,
            ...         temperature_ctd=1.075,
            ...         dissolved_o2=463.55,
            ...         temperature_do=1.12,
            ...         pressure=0.54
            ...     )
            ...     response = await client.send(sensor_slug="aml-ctd", data=reading)
            ...     print(f"Stored reading ID: {response.id}")
            >>>
            >>> asyncio.run(main())
        """
        url = f"{self.base_url}/api/sensors/ctd/{sensor_slug}/data"

        # Convert DTO to JSON dict
        payload = data.model_dump(mode="json", exclude_none=True)

        if self.verbose:
            logger.debug(f"Sending AML CTD sensor reading to {url}")
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
                return AMLCTDSensorReadingResponse(**response_data)

        except httpx.TimeoutException as e:
            raise RequestError(f"Request timed out after {self.timeout}s") from e
        except httpx.RequestError as e:
            raise RequestError(f"Request failed: {str(e)}") from e
