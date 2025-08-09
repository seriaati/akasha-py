from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import akasha

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@pytest.fixture
async def api() -> AsyncGenerator[akasha.AkashaAPI]:
    async with akasha.AkashaAPI() as api:
        yield api
