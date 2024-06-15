from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


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


class Leaderboard(BaseModel):
    id: str = Field(alias="_id")
    calculation: LeaderboardCalc
    character_id: int = Field(alias="characterId")
    build_name: str = Field(alias="type")
    uid: str
    owner: LeaderboardOwner
    rank: int = Field(alias="index")
