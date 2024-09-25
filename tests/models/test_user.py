from __future__ import annotations

import akasha


async def test_refresh_user() -> None:
    async with akasha.AkashaAPI() as api:
        await api.refresh_user(901211014)
