from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import akasha


async def test_refresh_user(api: akasha.AkashaAPI) -> None:
    await api.refresh_user(901211014)
