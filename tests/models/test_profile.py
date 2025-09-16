from __future__ import annotations

import pytest

import akasha


@pytest.mark.parametrize("sort_by", list(akasha.ProfileSortBy))
@pytest.mark.parametrize("order_by", list(akasha.OrderBy))
async def test_fetch_profiles(
    api: akasha.AkashaAPI, sort_by: akasha.ProfileSortBy, order_by: akasha.OrderBy
) -> None:
    await api._fetch_profiles(
        sort_by=sort_by, order_by=order_by, page=1, page_size=20, p="", from_id="", use_cache=False
    )


@pytest.mark.parametrize("sort_by", list(akasha.ProfileSortBy))
@pytest.mark.parametrize("order_by", list(akasha.OrderBy))
async def test_fetch_profiles_with_pagination(
    api: akasha.AkashaAPI, sort_by: akasha.ProfileSortBy, order_by: akasha.OrderBy
) -> None:
    async for profile in api.get_profiles(sort_by=sort_by, order_by=order_by, use_cache=False):
        assert profile.id
