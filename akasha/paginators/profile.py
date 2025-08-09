from __future__ import annotations

from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from akasha.enums import OrderBy, ProfileSortBy
    from akasha.models.profile import Profile


class ProfilePaginator:
    def __init__(
        self,
        fetcher: Callable[
            [ProfileSortBy, OrderBy, int, int, str, str, bool], Awaitable[list[Profile]]
        ],
        *,
        sort_by: ProfileSortBy,
        order_by: OrderBy,
        page_size: int,
        max_page: int,
        use_cache: bool,
    ) -> None:
        self._fetcher = fetcher
        self._profiles: list[Profile] = []

        self._page = 1
        self._index = 0

        self._sort_by = sort_by
        self._order_by = order_by

        self._page_size = page_size
        self._max_page = max_page
        self._use_cache = use_cache

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> Profile:
        if self._max_page < 0:
            msg = "max_page must be greater than 0"
            raise ValueError(msg)

        if self._index >= len(self._profiles) - 1:
            if self._page > self._max_page:
                raise StopAsyncIteration

            self._profiles = await self._fetcher(
                self._sort_by,
                self._order_by,
                self._page,
                self._page_size,
                f"lt|{self._profiles[-1].player_info.stygian_score}" if self._profiles else "",
                self._profiles[-1].id if self._profiles else "",
                self._use_cache,
            )
            self._index = 0
            self._page += 1
        else:
            self._index += 1

        try:
            return self._profiles[self._index]
        except IndexError as e:
            raise StopAsyncIteration from e
