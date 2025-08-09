from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import akasha


async def test_leaderboard(api: akasha.AkashaAPI) -> None:
    async for board in api.get_leaderboards(1000000203, max_page=1):
        assert board.uid


async def test_leaderboard_uids(api: akasha.AkashaAPI) -> None:
    async for board in api.get_leaderboards(
        1000000203, max_page=1, uids=(626792307, 730208419, 806331997)
    ):
        assert board.uid


async def test_leaderboard_variant(api: akasha.AkashaAPI) -> None:
    async for board in api.get_leaderboards(1000008921, max_page=1, variant="120er"):
        assert board.uid


async def test_leaderboard_total_size(api: akasha.AkashaAPI) -> None:
    await api.get_leaderboard_total_size(1000009808)
