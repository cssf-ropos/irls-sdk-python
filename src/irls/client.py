"""Main IRLS client."""

from irls.sensors.aml_ctd import AMLCTDSensorClient, AsyncAMLCTDSensorClient
from irls.sensors.position import AsyncPositionSensorClient, PositionSensorClient


class IRLSClient:
    """Main synchronous client for IRLS API.

    This is the primary entry point for interacting with IRLS. It provides
    access to sensor-specific clients for different sensor types.

    Args:
        base_url: Base URL of the IRLS instance (e.g., "http://127.0.0.1:8000")
        timeout: Request timeout in seconds (default: 30.0)
        verbose: Enable verbose logging for debugging (default: False)

    Example for position sensor:
        >>> from irls import IRLSClient
        >>> from irls.dto import PositionSensorReadingDTO
        >>> from datetime import datetime, timezone
        >>>
        >>> client = IRLSClient(base_url="http://127.0.0.1:8000")
        >>>
        >>> reading = PositionSensorReadingDTO(
        ...     recorded_at=datetime.now(timezone.utc),
        ...     x=-122.4194,
        ...     y=37.7749,
        ...     altitude=10.5,
        ...     heading=45.2,
        ...     satellite_count=12
        ... )
        >>>
        >>> response = client.position.send(sensor_slug="rovins", data=reading)
        >>> print(f"Success! Reading ID: {response.id}")
    """

    def __init__(self, base_url: str, timeout: float = 30.0, verbose: bool = False) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.verbose = verbose

        # Initialize sensor clients
        self._position = PositionSensorClient(base_url=base_url, timeout=timeout, verbose=verbose)
        self._amlctd = AMLCTDSensorClient(base_url=base_url, timeout=timeout, verbose=verbose)

    @property
    def amlctd(self) -> AMLCTDSensorClient:
        """Access the CTD sensor client.

        Returns:
            AMLCTDSensorClient for sending CTD sensor data
        Example:
            >>> client = IRLSClient(base_url="http://127.0.0.1:8000")
            >>> response = client.amlctd.send(sensor_slug="rovins", data=reading)
        """
        return self._amlctd

    @property
    def position(self) -> PositionSensorClient:
        """Access the position sensor client.

        Returns:
            PositionSensorClient for sending position sensor data

        Example:
            >>> client = IRLSClient(base_url="http://127.0.0.1:8000")
            >>> response = client.position.send(sensor_slug="rovins", data=reading)
        """
        return self._position


class AsyncIRLSClient:
    """Main asynchronous client for IRLS API.

    This client provides async operations for high-performance applications.
    Use this when you need to send many readings concurrently or integrate
    with async frameworks.

    Args:
        base_url: Base URL of the IRLS instance (e.g., "http://127.0.0.1:8000")
        timeout: Request timeout in seconds (default: 30.0)
        verbose: Enable verbose logging for debugging (default: False)

    Example:
        >>> import asyncio
        >>> from irls import AsyncIRLSClient
        >>> from irls.dto import PositionSensorReadingDTO
        >>> from datetime import datetime, timezone
        >>>
        >>> async def main():
        ...     client = AsyncIRLSClient(base_url="http://127.0.0.1:8000")
        ...
        ...     reading = PositionSensorReadingDTO(
        ...         recorded_at=datetime.now(timezone.utc),
        ...         x=-122.4194,
        ...         y=37.7749,
        ...         altitude=10.5
        ...     )
        ...
        ...     response = await client.position.send(sensor_slug="rovins", data=reading)
        ...     print(f"Success! Reading ID: {response.id}")
        >>>
        >>> asyncio.run(main())
    """

    def __init__(self, base_url: str, timeout: float = 30.0, verbose: bool = False) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.verbose = verbose

        # Initialize async sensor clients
        self._position = AsyncPositionSensorClient(
            base_url=base_url, timeout=timeout, verbose=verbose
        )
        self._amlctd = AsyncAMLCTDSensorClient(base_url=base_url, timeout=timeout, verbose=verbose)

    @property
    def amlctd(self) -> AsyncAMLCTDSensorClient:
        """Access the async CTD sensor client.

        Returns:
            AsyncAMLCTDSensorClient for sending CTD sensor data
        Example:
            >>> client = AsyncIRLSClient(base_url="http://127.0.0.1:8000")
            >>> response = await client.amlctd.send(sensor_slug="rovins", data=reading)
        """
        return self._amlctd

    @property
    def position(self) -> AsyncPositionSensorClient:
        """Access the async position sensor client.

        Returns:
            AsyncPositionSensorClient for sending position sensor data

        Example:
            >>> client = AsyncIRLSClient(base_url="http://127.0.0.1:8000")
            >>> response = await client.position.send(sensor_slug="rovins", data=reading)
        """
        return self._position
