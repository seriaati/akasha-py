from __future__ import annotations

from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Sequence

    from akasha.models.leaderboard import Leaderboard, StygianLeaderboard


class LeaderboardPaginator:
    def __init__(
        self,
        fetch_boards: Callable[
            [int, int, int, str, str | None, Sequence[int] | None, bool],
            Awaitable[list[Leaderboard]],
        ],
        calculation_id: int,
        page_size: int,
        max_page: int,
        variant: str | None,
        uids: Sequence[int] | None,
        use_cache: bool,
    ) -> None:
        self._fetch_boards = fetch_boards
        self._boards: list[Leaderboard] = []

        self._calculation_id = calculation_id
        self._page = 1
        self._index = 0
        self._page_size = page_size
        self._max_page = max_page
        self._variant = variant
        self._uids = uids
        self._use_cache = use_cache

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> Leaderboard:
        if self._max_page < 0:
            msg = "max_page must be greater than 0"
            raise ValueError(msg)

        if self._index >= len(self._boards) - 1:
            if self._page > self._max_page:
                raise StopAsyncIteration
            self._boards = await self._fetch_boards(
                self._calculation_id,
                self._page,
                self._page_size,
                f"lt|{self._boards[-1].calculation.result}" if self._boards else "",
                self._variant,
                self._uids,
                self._use_cache,
            )
            self._index = 0
            self._page += 1
        else:
            self._index += 1

        try:
            return self._boards[self._index]
        except IndexError as e:
            raise StopAsyncIteration from e


class StygianLeaderboardPaginator:
    def __init__(
        self,
        fetch_boards: Callable[
            [int, int, str, str, Sequence[int] | None, bool],
            Awaitable[list[StygianLeaderboard]],
        ],
        version: str,
        page_size: int,
        max_page: int,
        uids: Sequence[int] | None,
        use_cache: bool,
    ) -> None:
        self._fetch_boards = fetch_boards
        self._boards: list[StygianLeaderboard] = []

        self._version = version
        self._page = 1
        self._index = 0
        self._page_size = page_size
        self._max_page = max_page
        self._uids = uids
        self._use_cache = use_cache

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> StygianLeaderboard:
        if self._max_page < 0:
            msg = "max_page must be greater than 0"
            raise ValueError(msg)

        if self._index >= len(self._boards) - 1:
            if self._page > self._max_page:
                raise StopAsyncIteration
            self._boards = await self._fetch_boards(
                self._page,
                self._page_size,
                f"lt|{self._boards[-1].stygian_score}" if self._boards else "",
                self._version,
                self._uids,
                self._use_cache,
            )
            self._index = 0
            self._page += 1
        else:
            self._index += 1

        try:
            return self._boards[self._index]
        except IndexError as e:
            raise StopAsyncIteration from e
