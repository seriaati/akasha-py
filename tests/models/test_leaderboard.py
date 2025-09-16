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


async def test_stygian_leaderboard(api: akasha.AkashaAPI) -> None:
    async for board in api.get_stygian_leaderboards("5_8", max_page=1):
        assert board.uid
        assert board.stygian_score
        assert board.stygian_seconds
        assert board.stygian_index
        assert board.owner
        assert board.player_info


async def test_stygian_leaderboard_uids(api: akasha.AkashaAPI) -> None:
    async for board in api.get_stygian_leaderboards("5_8", max_page=1, uids=(626792307, 730208419)):
        assert board.uid
        assert int(board.uid) in {626792307, 730208419}


async def test_stygian_leaderboard_page_size(api: akasha.AkashaAPI) -> None:
    boards = []
    async for board in api.get_stygian_leaderboards("5_8", max_page=1, page_size=5):
        boards.append(board)
    assert len(boards) <= 5
