from __future__ import annotations

import akasha


async def test_multi_translate() -> None:
    for lang in akasha.Language:
        if lang is akasha.Language.ENGLISH:
            continue
        async with akasha.AkashaAPI(lang) as api:
            await api.get_translations(["Kamisato Ayaka", "Mistsplitter Reforged"])


async def test_single_translate() -> None:
    for lang in akasha.Language:
        if lang is akasha.Language.ENGLISH:
            continue
        async with akasha.AkashaAPI(lang) as api:
            await api.translate("Kamisato Ayaka")
