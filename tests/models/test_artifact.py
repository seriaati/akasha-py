from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import akasha


async def test_get_artifact(api: akasha.AkashaAPI) -> None:
    await api.get_artifacts(820863575, "69313a2a03491ee368aa75837d1da7af")
