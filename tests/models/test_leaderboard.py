from __future__ import annotations

import akasha


async def test_leaderboard() -> None:
    async with akasha.AkashaAPI() as api:
        async for board in api.get_leaderboards(1000000203, max_page=1):
            assert board.uid


async def test_leaderboard_for_uid() -> None:
    async with akasha.AkashaAPI() as api:
        data = await api.get_leaderboard_for_uids(1000009808, uids=901211014)
        assert data and data.uid == "901211014"


async def test_leaderboard_for_uids() -> None:
    async with akasha.AkashaAPI() as api:
        data = await api.get_leaderboard_for_uids(1000009808, uids=(901211014, 901211015))
        assert data
        assert data[0].uid == "901211014"


async def test_leaderboard_total_size() -> None:
    async with akasha.AkashaAPI() as api:
        await api.get_leaderboard_total_size(1000009808)
