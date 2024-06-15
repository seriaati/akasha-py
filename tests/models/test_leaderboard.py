import akasha


async def test_leaderboard() -> None:
    async with akasha.AkashaAPI() as api:
        await api.get_leaderboards(1000000203)
