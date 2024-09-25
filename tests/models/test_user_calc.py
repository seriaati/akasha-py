from __future__ import annotations

import akasha


async def test_user_calc() -> None:
    async with akasha.AkashaAPI() as api:
        await api.get_calculations_for_user(901211014)


async def test_non_existent_user() -> None:
    async with akasha.AkashaAPI() as api:
        await api.get_calculations_for_user(0)
