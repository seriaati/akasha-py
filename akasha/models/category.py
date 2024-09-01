import datetime
from typing import Literal

from pydantic import BaseModel, Field

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
    constellation: Literal[0, 1, 2, 3, 4, 5, 6]


class TeammateWeapon(BaseModel):
    name: str
    rarity: Literal[1, 2, 3, 4, 5]
    icon: str
    refinement: Literal[1, 2, 3, 4, 5]


class LeaderboardTeammate(BaseModel):
    character: TeammateCharacter
    weapon: TeammateWeapon


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


class LeaderboardCategory(BaseModel):
    id: str = Field(alias="_id")
    added_date: datetime.datetime = Field(alias="addDate")
    character_id: int = Field(alias="characterId")
    character_name: str = Field(alias="characterName")

    count: int
    details: str
    element: str
    name: str
    rarity: int
    short_name: str = Field(alias="short")
    character_icon: str = Field(alias="characterIcon")
    index: int
