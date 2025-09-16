from __future__ import annotations

import datetime

from pydantic import BaseModel, Field, field_validator


class NameCardAsset(BaseModel):
    icon: str
    pictures: list[str] = Field(alias="picPath")

    @field_validator("icon", mode="after")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://enka.network/ui/{v}.png"

    @field_validator("pictures", mode="after")
    @classmethod
    def __convert_pictures(cls, v: list[str]) -> list[str]:
        return [f"https://enka.network/ui/{i}.png" for i in v]


class NameCard(BaseModel):
    name: str | None = None
    id: int
    asset: NameCardAsset = Field(alias="assets")


class PlayerInfo(BaseModel):
    nickname: str
    level: int
    signature: str | None = None
    region: str
    name_card: NameCard | int = Field(alias="nameCardId")

    world_level: int | None = Field(default=None, alias="worldLevel")
    achievement_count: int = Field(alias="finishAchievementNum")
    """Number of achievements completed."""

    abyss_floor: int | None = Field(alias="towerFloorIndex", default=None)
    abyss_level: int | None = Field(alias="towerLevelIndex", default=None)

    stygian_index: int | None = Field(alias="stygianIndex", default=None)
    stygian_seconds: int | None = Field(alias="stygianSeconds", default=None)
    stygian_score: float | None = Field(alias="stygianScore", default=None)

    max_friendship_count: int = Field(alias="maxFriendshipNum", default=0)
    """Number of max friendship characters this player has."""

    @field_validator("level", mode="before")
    @classmethod
    def __convert_level(cls, v: float) -> int:
        return int(v)

    @field_validator("achievement_count", mode="before")
    @classmethod
    def __convert_achievement_count(cls, v: float) -> int:
        return int(v)

    @field_validator("world_level", "abyss_floor", "abyss_level", mode="before")
    @classmethod
    def __parse_invalid_values(cls, v: str | int) -> int:
        if isinstance(v, str):
            return 0
        return v


class Profile(BaseModel):
    index: int
    id: str = Field(alias="_id")
    uid: str
    player_info: PlayerInfo = Field(alias="playerInfo")

    owned_character_ids: list[int] = Field(alias="ownedCharacters", default_factory=list)
    updated_at: datetime.datetime | None = Field(alias="lastProfileUpdate", default=None)

    profile_picture_url: str = Field(alias="profilePictureLink")
    name_card_url: str = Field(alias="nameCardLink")
