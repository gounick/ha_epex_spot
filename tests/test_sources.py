"""Network smoke tests for public epex_spot data sources."""

import asyncio
import importlib
from dataclasses import dataclass

import aiohttp
import pytest


@dataclass
class _SourceSpec:
    module: str
    cls: str


PUBLIC_SOURCES = [
    _SourceSpec("custom_components.epex_spot.EPEXSpot.Awattar", "Awattar"),
    _SourceSpec("custom_components.epex_spot.EPEXSpot.EnergyCharts", "EnergyCharts"),
    _SourceSpec("custom_components.epex_spot.EPEXSpot.EnergyZero", "EnergyZero"),
    _SourceSpec(
        "custom_components.epex_spot.EPEXSpot.HoferGruenstrom", "HoferGruenstrom"
    ),
    _SourceSpec("custom_components.epex_spot.EPEXSpot.SMARD", "SMARD"),
    _SourceSpec("custom_components.epex_spot.EPEXSpot.smartENERGY", "smartENERGY"),
]


def _load_source(spec: _SourceSpec):
    module = importlib.import_module(spec.module)
    return getattr(module, spec.cls)


def _build_params():
    params = []
    for spec in PUBLIC_SOURCES:
        source = _load_source(spec)
        for market_area in source.MARKET_AREAS:
            for duration in source.SUPPORTED_DURATIONS:
                params.append(
                    pytest.param(
                        spec,
                        market_area,
                        duration,
                        id=f"{spec.cls}-{market_area}-{duration}min",
                    )
                )
    return params


@pytest.mark.parametrize(
    ("spec", "market_area", "duration"),
    _build_params(),
)
@pytest.mark.asyncio
async def test_source_fetch(spec: _SourceSpec, market_area: str, duration: int) -> None:
    """Check that configured source URLs are reachable and do not return 404.

    Temporary network failures are skipped; only HTTP 404 is treated as a
    mapping/configuration error.

    :param spec: Source module/class specification.
    :param market_area: Market area to test.
    :param duration: Duration in minutes to test.
    """
    source_cls = _load_source(spec)

    async with aiohttp.ClientSession() as session:
        source = source_cls(
            market_area=market_area,
            duration=duration,
            session=session,
        )

        try:
            await asyncio.wait_for(source.fetch(), timeout=30)
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                pytest.fail(
                    f"Source {spec.cls} ({market_area}, {duration}min) "
                    f"returned 404 for {err.request_info.url}"
                )
            pytest.skip(f"HTTP {err.status} from {err.request_info.url}")
        except (TimeoutError, aiohttp.ClientError):
            pytest.skip("Network or API temporarily unavailable")
