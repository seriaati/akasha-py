import akasha


async def test_refresh_user() -> None:
    async with akasha.AkashaAPI() as api:
        await api.refresh_user(901211014)


async def test_get_user() -> None:
    async with akasha.AkashaAPI() as api:
        await api.get_user(901211014)
