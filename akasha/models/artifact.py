from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from ..enums import EquipType

__all__ = ("Artifact", "ArtifactStat")


class ArtifactStat(BaseModel):
    name: str
    value: float


class Artifact(BaseModel):
    name: str
    set_name: str = Field(alias="setName")
    rarity: int = Field(alias="stars")
    main_stat: ArtifactStat
    substats: list[ArtifactStat]
    equip_type: EquipType = Field(alias="equipType")
    level: int
    crit_value: float = Field(alias="critValue")
    icon: str

    @field_validator("substats", mode="before")
    @classmethod
    def __transform_substats(cls, v: dict[str, float]) -> list[ArtifactStat]:
        return [ArtifactStat(name=name, value=value) for name, value in v.items()]

    @model_validator(mode="before")
    @classmethod
    def __transform_main_stat(cls, v: dict[str, Any]) -> dict[str, Any]:
        v["main_stat"] = {"name": v.pop("mainStatKey"), "value": v.pop("mainStatValue")}
        return v
