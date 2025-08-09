from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import akasha


async def test_user_calc(api: akasha.AkashaAPI) -> None:
    await api.get_calculations_for_user(901211014)


async def test_non_existent_user(api: akasha.AkashaAPI) -> None:
    await api.get_calculations_for_user(0)
