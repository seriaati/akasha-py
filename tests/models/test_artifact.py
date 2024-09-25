from __future__ import annotations

import akasha


async def test_get_artifact() -> None:
    async with akasha.AkashaAPI() as api:
        await api.get_artifacts(820863575, "69313a2a03491ee368aa75837d1da7af")
