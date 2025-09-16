from __future__ import annotations

import pytest

import akasha
from akasha.models.profile import NameCardAsset, PlayerInfo


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


def test_name_card_asset_icon_url_conversion() -> None:
    """Test NameCardAsset icon URL conversion."""
    data = {
        "icon": "UI_NameCardIcon_0",
        "picPath": ["UI_NameCardPic_Kazuha_P", "UI_NameCardPic_Kazuha_Alpha"],
    }

    asset = NameCardAsset(**data)

    assert asset.icon == "https://enka.network/ui/UI_NameCardIcon_0.png"
    assert asset.pictures == [
        "https://enka.network/ui/UI_NameCardPic_Kazuha_P.png",
        "https://enka.network/ui/UI_NameCardPic_Kazuha_Alpha.png",
    ]


def test_player_info_name_card_field() -> None:
    """Test PlayerInfo with nameCard field."""
    data = {
        "nickname": "TestPlayer",
        "level": 60,
        "signature": "Test signature",
        "region": "North America",
        "nameCardId": {
            "id": 210001,
            "name": "Travel Notes: Catch the Wind",
            "assets": {
                "icon": "UI_NameCardIcon_0",
                "picPath": ["UI_NameCardPic_0_P", "UI_NameCardPic_0_Alpha"],
            },
        },
        "finishAchievementNum": 42,
    }

    player_info = PlayerInfo(**data)

    assert player_info.name_card.id == 210001
    assert player_info.name_card.name == "Travel Notes: Catch the Wind"
    assert player_info.name_card.asset.icon == "https://enka.network/ui/UI_NameCardIcon_0.png"


def test_player_info_optional_world_level() -> None:
    """Test PlayerInfo with optional world_level field."""
    # Test with world_level present
    data_with_wl = {
        "nickname": "TestPlayer",
        "level": 60,
        "region": "Asia",
        "nameCardId": {
            "id": 210001,
            "name": "Travel Notes",
            "assets": {"icon": "UI_NameCardIcon_0", "picPath": []},
        },
        "worldLevel": 8,
        "finishAchievementNum": 100,
    }

    player_info_with_wl = PlayerInfo(**data_with_wl)
    assert player_info_with_wl.world_level == 8

    # Test without world_level
    data_without_wl = {
        "nickname": "TestPlayer",
        "level": 60,
        "region": "Asia",
        "nameCardId": {
            "id": 210001,
            "name": "Travel Notes",
            "assets": {"icon": "UI_NameCardIcon_0", "picPath": []},
        },
        "finishAchievementNum": 100,
    }

    player_info_without_wl = PlayerInfo(**data_without_wl)
    assert player_info_without_wl.world_level is None
