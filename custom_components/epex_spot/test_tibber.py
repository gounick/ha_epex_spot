#!/usr/bin/env python3

import asyncio

import aiohttp

from .const import TIBBER_DEMO_TOKEN, UOM_EUR_PER_KWH
from .EPEXSpot import Tibber


async def main():
    async with aiohttp.ClientSession() as session:
        durations = [15, 60]
        for duration in durations:
            service = Tibber.Tibber(
                market_area="de",
                token=TIBBER_DEMO_TOKEN,
                session=session,
                duration=duration,
            )
            print(service.MARKET_AREAS)

            await service.fetch()
            print(f"duration={duration} count = {len(service.marketdata)}")
            for e in service.marketdata:
                print(f"{e.start_time}: {e.market_price_per_kwh} {UOM_EUR_PER_KWH}")


asyncio.run(main())
