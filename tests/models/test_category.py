from __future__ import annotations

import akasha


async def test_get_categories() -> None:
    async with akasha.AkashaAPI() as api:
        await api.get_categories("10000098")
