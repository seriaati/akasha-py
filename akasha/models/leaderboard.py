from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from akasha.enums import Element

__all__ = ("Leaderboard", "LeaderboardCalc", "LeaderboardOwner", "ProfilePicture")


class LeaderboardCalc(BaseModel):
    id: str
    result: float


class ProfilePicture(BaseModel):
    icon: str
    old_icon: str | None = Field(None, alias="oldIcon")

    @field_validator("icon", "old_icon", mode="after")
    @classmethod
    def __convert_icon(cls, v: str) -> str:
        return f"https://enka.network/ui/{v}.png"

    @model_validator(mode="before")
    @classmethod
    def __flatten_assets(cls, v: dict[str, Any]) -> dict[str, Any]:
        assets = v.pop("assets", {})
        return {**v, **assets}


class LeaderboardOwner(BaseModel):
    nickname: str
    adventure_rank: int = Field(alias="adventureRank")
    profile_picture: ProfilePicture = Field(alias="profilePicture")
    namecard: str = Field(alias="nameCard")
    region: str

    @field_validator("adventure_rank", mode="before")
    @classmethod
    def __intify_adventure_rank(cls, v: float) -> int:
        return int(v)

    @field_validator("namecard", mode="after")
    @classmethod
    def __convert_namecard(cls, v: str) -> str:
        return f"https://enka.network/ui/{v}.png"


class CharacterTalent(BaseModel):
    icon: str
    level: int
    raw_level: int = Field(alias="rawLevel")
    id: int
    boosted: bool


class CharacterWeapon(BaseModel):
    level: int
    ascension: int = Field(alias="promoteLevel")
    refinement: int
    icon: str
    name: str

    @model_validator(mode="before")
    @classmethod
    def __unnest_weapon_info(cls, v: dict[str, Any]) -> dict[str, Any]:
        weapon_info = v.pop("weaponInfo")
        v["level"] = weapon_info["level"]
        v["promoteLevel"] = weapon_info["promoteLevel"]
        v["refinement"] = weapon_info["refinementLevel"]["value"]
        return v


class Leaderboard(BaseModel):
    id: str = Field(alias="_id")
    calculation: LeaderboardCalc
    build_name: str = Field(alias="type")
    uid: str
    owner: LeaderboardOwner
    rank: int = Field(alias="index")
    md5: str

    # Character related fields
    character_id: int = Field(alias="characterId")
    constellation: int
    crit_value: float = Field(alias="critValue")
    ascension: int
    level: int
    stats: dict[str, float]
    talents: dict[str, CharacterTalent] = Field(alias="talentsLevelMap")
    weapon: CharacterWeapon
    element: Element = Field(alias="characterMetadata")

    @field_validator("stats", mode="before")
    @classmethod
    def __unnest_stats_value(cls, v: dict[str, dict[str, float]]) -> dict[str, float]:
        return {k: v["value"] for k, v in v.items()}

    @field_validator("element", mode="before")
    @classmethod
    def __unnest_element(cls, v: dict[str, str]) -> str:
        return v["element"]

    @model_validator(mode="before")
    @classmethod
    def __unnest_fields(cls, v: dict[str, Any]) -> dict[str, Any]:
        prop_map = v.pop("propMap")
        v["ascension"] = int(prop_map["ascension"]["val"])
        v["level"] = int(prop_map["level"]["val"])
        return v
