from __future__ import annotations

from enum import StrEnum

__all__ = ("ArtifactStat", "CharaStatType", "Element", "EquipType", "Language")


class Language(StrEnum):
    """Languages supported by Akasha System."""

    ENGLISH = "en"
    GERMAN = "de"
    FRENCH = "fr"
    SPANISH = "es"
    ITALIAN = "it"
    JAPANESE = "ja"
    KOREAN = "ko"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    THAI = "th"
    TURKISH = "tr"
    VIETNAMESE = "vi"
    CHINESE_SIMPLIFIED = "zh-CN"
    CHINESE_TRADITIONAL = "zh-TW"


class EquipType(StrEnum):
    """Artifact types."""

    FLOWER = "EQUIP_BRACER"
    FEATHER = "EQUIP_NECKLACE"
    SANDS = "EQUIP_SHOES"
    GOBLET = "EQUIP_RING"
    CIRCLET = "EQUIP_DRESS"


class Element(StrEnum):
    """Elements in Genshin Impact."""

    HYDRO = "Hydro"
    ANEMO = "Anemo"
    PYRO = "Pyro"
    CRYO = "Cryo"
    ELECTRO = "Electro"
    GEO = "Geo"
    DENDRO = "Dendro"


class ArtifactStat(StrEnum):
    """Artifact stat names."""

    CRIT_DMG = "Crit DMG"
    CRIT_RATE = "Crit RATE"

    FLAT_HP = "Flat HP"
    HP_PERCENT = "HP%"
    FLAT_ATK = "Flat ATK"
    ATK_PERCENT = "ATK%"
    FLAT_DEF = "Flat DEF"
    DEF_PERCENT = "DEF%"

    ENERGY_RECHARGE = "Energy Recharge"
    ELEMENTAL_MASTERY = "Elemental Mastery"

    HYDRO_DMG_BONUS = "Hydro DMG Bonus"
    ANEMO_DMG_BONUS = "Anemo DMG Bonus"
    PYRO_DMG_BONUS = "Pyro DMG Bonus"
    CRYO_DMG_BONUS = "Cryo DMG Bonus"
    ELECTRO_DMG_BONUS = "Electro DMG Bonus"
    GEO_DMG_BONUS = "Geo DMG Bonus"
    DENDRO_DMG_BONUS = "Dendro DMG Bonus"


class CharaStatType(StrEnum):
    """Character stat types."""

    MAX_HP = "maxHp"
    ATK = "atk"
    DEF = "def"
    ELEMENTAL_MASTERY = "elementalMastery"
    ENERGY_RECHARGE = "energyRecharge"
    HEALING_BONUS = "healingBonus"
    CRIT_RATE = "critRate"
    CRIT_DMG = "critDamage"

    CRYO_DMG_BONUS = "cryoDamageBonus"
    PYRO_DMG_BONUS = "pyroDamageBonus"
    HYDRO_DMG_BONUS = "hydroDamageBonus"
    ANEMO_DMG_BONUS = "anemoDamageBonus"
    ELECTRO_DMG_BONUS = "electroDamageBonus"
    GEO_DMG_BONUS = "geoDamageBonus"
    DENDRO_DMG_BONUS = "dendroDamageBonus"
    PHYSICAL_DMG_BONUS = "physicalDamageBonus"
