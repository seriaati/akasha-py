import akasha


async def test_leaderboard() -> None:
    async with akasha.AkashaAPI() as api:
        async for board in api.get_leaderboards(1000000203, max_page=1):
            assert board.uid


async def test_leaderboard_for_uid() -> None:
    async with akasha.AkashaAPI() as api:
        data = await api.get_leaderboard_for_uid(1000009808, uid=901211014)
        assert data.uid == "901211014"
