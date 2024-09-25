from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, computed_field, field_validator, model_validator

from akasha.constants import PERCENT_STAT_TYPES

from .. import enums

__all__ = ("Artifact", "ArtifactStat")


class ArtifactStat(BaseModel):
    type: enums.ArtifactStat = Field(alias="name")
    value: float

    @computed_field
    @property
    def display_value(self) -> str:
        if self.type in PERCENT_STAT_TYPES:
            return f"{self.value * 100:.1f}%"
        return str(round(self.value))


class Artifact(BaseModel):
    name: str
    set_name: str = Field(alias="setName")
    rarity: int = Field(alias="stars")
    main_stat: ArtifactStat
    substats: list[ArtifactStat]
    equip_type: enums.EquipType = Field(alias="equipType")
    level: int
    crit_value: float = Field(alias="critValue")
    icon: str

    @field_validator("substats", mode="before")
    @classmethod
    def __transform_substats(cls, v: dict[str, float]) -> list[ArtifactStat]:
        return [
            ArtifactStat(name=enums.ArtifactStat(name), value=value) for name, value in v.items()
        ]

    @field_validator("level", mode="before")
    @classmethod
    def __subtract_level(cls, v: int) -> int:
        return v - 1

    @model_validator(mode="before")
    @classmethod
    def __transform_main_stat(cls, v: dict[str, Any]) -> dict[str, Any]:
        v["main_stat"] = {"name": v.pop("mainStatKey"), "value": v.pop("mainStatValue")}
        return v
