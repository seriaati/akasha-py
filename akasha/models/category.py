from __future__ import annotations

import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

__all__ = (
    "LeaderboardCategory",
    "LeaderboardTeammate",
    "TeammateCharacter",
    "TeammateWeapon",
    "WeaponLeaderboard",
)


class TeammateCharacter(BaseModel):
    name: str
    element: str
    rarity: Literal[4, 5]
    icon: str
    constellation: Literal[0, 1, 2, 3, 4, 5, 6] | None


class TeammateWeapon(BaseModel):
    name: str
    rarity: Literal[1, 2, 3, 4, 5]
    icon: str
    refinement: Literal[1, 2, 3, 4, 5]


class LeaderboardTeammate(BaseModel):
    character: TeammateCharacter
    weapon: TeammateWeapon | None = None


class WeaponLeaderboardFilter(BaseModel):
    id: str = Field(alias="name")
    name: str = Field(alias="displayName")


class WeaponLeaderboard(BaseModel):
    name: str
    icon: str
    substat: str
    rarity: Literal[1, 2, 3, 4, 5]
    refinement: Literal[1, 2, 3, 4, 5]
    calculation_id: str = Field(alias="calculationId")
    details: str
    short_name: str = Field(alias="short")
    teammates: list[LeaderboardTeammate]
    filters: list[WeaponLeaderboardFilter]

    @field_validator("teammates", mode="before")
    @classmethod
    def __parse_teammates(cls, v: list[dict[str, Any]]) -> list[LeaderboardTeammate]:
        return [LeaderboardTeammate(**teammate) for teammate in v if "name" in teammate]

    @field_validator("filters", mode="before")
    @classmethod
    def __parse_filters(cls, v: list[dict[str, Any]] | None) -> list[WeaponLeaderboardFilter]:
        return [WeaponLeaderboardFilter(**filter_) for filter_ in v] if v else []


class LeaderboardCategory(BaseModel):
    id: str = Field(alias="_id")
    added_date: datetime.datetime = Field(alias="addDate")
    character_id: int = Field(alias="characterId")
    character_name: str = Field(alias="characterName")
    weapons: list[WeaponLeaderboard]

    count: int
    details: str
    element: str
    name: str
    rarity: int
    short_name: str = Field(alias="short")
    character_icon: str = Field(alias="characterIcon")
    index: int
