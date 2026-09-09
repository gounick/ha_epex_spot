"""EnergyZero API Client."""

import logging
from datetime import UTC, datetime, timedelta

import aiohttp

from ...common import Marketprice

_LOGGER = logging.getLogger(__name__)


class EnergyZero:
    """Client for EnergyZero dynamic electricity prices.

    EnergyZero provides public, authentication-free day-ahead electricity
    prices for the Netherlands in both hourly and quarter-hourly intervals.

    :param market_area: Market area identifier. Only ``NL`` is supported.
    :type market_area: str
    :param duration: Interval duration in minutes (15 or 60).
    :type duration: int
    :param session: aiohttp client session used for HTTP requests.
    :type session: aiohttp.ClientSession
    """

    URL = "https://api.energyzero.nl/v1/energyprices"

    MARKET_AREAS = ("NL",)
    SUPPORTED_DURATIONS = (15, 60)

    def __init__(
        self,
        market_area: str,
        duration: int,
        session: aiohttp.ClientSession,
    ):
        """Initialize the EnergyZero client."""
        if market_area not in self.MARKET_AREAS:
            raise ValueError(f"Unsupported market area: {market_area}")
        if duration not in self.SUPPORTED_DURATIONS:
            raise ValueError(f"Unsupported duration: {duration}")

        self._session = session
        self._market_area = market_area
        self._duration = duration
        self._marketdata: list[Marketprice] = []

    @property
    def name(self) -> str:
        """Return the source name.

        :return: Human-readable source name.
        :rtype: str
        """
        return "EnergyZero API"

    @property
    def market_area(self) -> str:
        """Return the configured market area.

        :return: Market area identifier.
        :rtype: str
        """
        return self._market_area

    @property
    def duration(self) -> int:
        """Return the configured interval duration.

        :return: Duration in minutes.
        :rtype: int
        """
        return self._duration

    @property
    def currency(self) -> str:
        """Return the price currency.

        :return: ISO 4217 currency code.
        :rtype: str
        """
        return "EUR"

    @property
    def marketdata(self) -> list[Marketprice]:
        """Return the fetched market data.

        :return: List of market price entries.
        :rtype: list[Marketprice]
        """
        return self._marketdata

    async def fetch(self) -> None:
        """Fetch prices from the EnergyZero API and populate marketdata."""
        data = await self._fetch_data()
        self._marketdata = self._extract_marketdata(data)

    async def _fetch_data(self) -> dict:
        """Request the price data from the EnergyZero REST API.

        A rolling two-day window starting from the current hour is requested
        so that today's and tomorrow's prices are available in one call.

        :return: Parsed JSON response from the API.
        :rtype: dict
        """
        start = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
        end = start + timedelta(days=2)

        params = {
            "fromDate": start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "tillDate": end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "interval": 3 if self._duration == 15 else 4,
            "usageType": 1,
            "inclBtw": "true",
        }

        async with self._session.get(self.URL, params=params) as resp:
            resp.raise_for_status()
            return await resp.json()

    def _extract_marketdata(self, data: dict) -> list[Marketprice]:
        """Convert the API JSON response into :class:`Marketprice` objects.

        :param data: Parsed JSON response from the API.
        :type data: dict
        :return: List of market price entries.
        :rtype: list[Marketprice]
        :raises TypeError: If the response format is not as expected.
        """
        if not isinstance(data, dict):
            raise TypeError("Unexpected EnergyZero API response format")

        prices = data.get("Prices", [])
        if not prices:
            _LOGGER.warning("EnergyZero API returned no prices")
            return []

        entries: list[Marketprice] = []
        for item in prices:
            start_time = datetime.fromisoformat(item["readingDate"])
            price = round(float(item["price"]), 6)
            entries.append(
                Marketprice(
                    start_time=start_time,
                    duration=self._duration,
                    price=price,
                )
            )
        return entries
