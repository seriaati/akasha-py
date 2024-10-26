from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, computed_field, field_validator

__all__ = ("CharacterCalc", "CharacterCalcWeapon", "UserCalc", "UserCalcArtifact")


class CharacterCalcWeapon(BaseModel):
    name: str
    icon: str
    substat: str
    type: str
    rarity: Literal[1, 2, 3, 4, 5]
    refinement: Literal[1, 2, 3, 4, 5]


class CharacterCalcVariant(BaseModel):
    name: str
    display_name: str = Field(alias="displayName")


class CharacterCalc(BaseModel):
    id: int = Field(alias="calculationId")
    short: str
    name: str
    details: str
    weapon: CharacterCalcWeapon
    result: float
    stats: dict[str, float] | None = None
    ranking: int
    out_of: int = Field(alias="outOf")
    variant: CharacterCalcVariant | None = None

    @computed_field
    @property
    def top_percent(self) -> float:
        return (self.ranking / self.out_of) * 100


class UserCalcArtifact(BaseModel):
    name: str
    icon: str
    count: int


class UserCalc(BaseModel):
    id: str = Field(alias="_id")
    character_id: int = Field(alias="characterId")
    type: str
    uid: str
    artifact_sets: list[UserCalcArtifact] = Field(alias="artifactSets")
    calculations: list[CharacterCalc]
    constellation: Literal[0, 1, 2, 3, 4, 5, 6]
    md5: str
    name: str
    icon: str

    @field_validator("artifact_sets", mode="before")
    @classmethod
    def __flatten_artifacts(cls, v: dict[str, Any]) -> list[UserCalcArtifact]:
        return [UserCalcArtifact(name=name, **artifact) for name, artifact in v.items()]

    @field_validator("calculations", mode="before")
    @classmethod
    def __flatten_calculations(cls, v: dict[str, Any] | None) -> list[CharacterCalc]:
        return [CharacterCalc(**calc) for calc in v.values()] if v is not None else []
