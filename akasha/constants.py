from __future__ import annotations

from .enums import ArtifactStat, CharaStatType

PERCENT_STAT_TYPES: set[CharaStatType | ArtifactStat] = {
    CharaStatType.CRIT_RATE,
    CharaStatType.CRIT_DMG,
    CharaStatType.CRYO_DMG_BONUS,
    CharaStatType.PYRO_DMG_BONUS,
    CharaStatType.HYDRO_DMG_BONUS,
    CharaStatType.ANEMO_DMG_BONUS,
    CharaStatType.ELECTRO_DMG_BONUS,
    CharaStatType.GEO_DMG_BONUS,
    CharaStatType.DENDRO_DMG_BONUS,
    CharaStatType.HEALING_BONUS,
    CharaStatType.ENERGY_RECHARGE,
    ArtifactStat.ENERGY_RECHARGE,
    ArtifactStat.CRIT_RATE,
    ArtifactStat.CRIT_DMG,
    ArtifactStat.HP_PERCENT,
    ArtifactStat.ATK_PERCENT,
    ArtifactStat.DEF_PERCENT,
    ArtifactStat.CRYO_DMG_BONUS,
    ArtifactStat.PYRO_DMG_BONUS,
    ArtifactStat.HYDRO_DMG_BONUS,
    ArtifactStat.ANEMO_DMG_BONUS,
    ArtifactStat.ELECTRO_DMG_BONUS,
    ArtifactStat.GEO_DMG_BONUS,
    ArtifactStat.DENDRO_DMG_BONUS,
}
