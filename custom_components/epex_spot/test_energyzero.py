#!/usr/bin/env python3
"""Standalone smoke test for the EnergyZero source."""

import asyncio

import aiohttp

from .const import UOM_EUR_PER_KWH
from .EPEXSpot import EnergyZero


async def main():
    """Fetch prices for both supported durations and print a summary."""
    for duration in (15, 60):
        print(f"\n=== Testing EnergyZero: {duration} minutes ===")
        async with aiohttp.ClientSession() as session:
            service = EnergyZero.EnergyZero(
                market_area="NL",
                duration=duration,
                session=session,
            )

            await service.fetch()
            print(f"count = {len(service.marketdata)}")
            for e in service.marketdata:
                print(f"{e.start_time}: {e.market_price_per_kwh} {UOM_EUR_PER_KWH}")


asyncio.run(main())
