from __future__ import annotations

import akasha


async def test_leaderboard() -> None:
    async with akasha.AkashaAPI() as api:
        async for board in api.get_leaderboards(1000000203, max_page=1):
            assert board.uid


async def test_leaderboard_uids() -> None:
    async with akasha.AkashaAPI() as api:
        async for board in api.get_leaderboards(
            1000000203, max_page=1, uids=(626792307, 730208419, 806331997)
        ):
            assert board.uid


async def test_leaderboard_variant() -> None:
    async with akasha.AkashaAPI() as api:
        async for board in api.get_leaderboards(1000008921, max_page=1, variant="120er"):
            assert board.uid


async def test_leaderboard_total_size() -> None:
    async with akasha.AkashaAPI() as api:
        await api.get_leaderboard_total_size(1000009808)
