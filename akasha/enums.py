from enum import StrEnum

__all__ = ("EquipType", "Language")


class Language(StrEnum):
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
    HYDRO = "Hydro"
    ANEMO = "Anemo"
    PYRO = "Pyro"
    CRYO = "Cryo"
    ELECTRO = "Electro"
    GEO = "Geo"
    DENDRO = "Dendro"
