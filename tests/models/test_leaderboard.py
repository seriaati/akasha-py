import akasha


async def test_leaderboard() -> None:
    async with akasha.AkashaAPI() as api:
        async for board in api.get_leaderboards(1000000203, max_page=1):
            assert board.uid
