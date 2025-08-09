from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import akasha


async def test_get_categories(api: akasha.AkashaAPI) -> None:
    await api.get_categories("10000098")
