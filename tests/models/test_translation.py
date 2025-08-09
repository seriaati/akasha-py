from __future__ import annotations

import pytest

import akasha


@pytest.mark.parametrize("lang", list(akasha.Language))
async def test_multi_translate(lang: akasha.Language) -> None:
    if lang is akasha.Language.ENGLISH:
        return
    async with akasha.AkashaAPI(lang) as api:
        await api.get_translations(["Kamisato Ayaka", "Mistsplitter Reforged"])


@pytest.mark.parametrize("lang", list(akasha.Language))
async def test_single_translate(lang: akasha.Language) -> None:
    if lang is akasha.Language.ENGLISH:
        return
    async with akasha.AkashaAPI(lang) as api:
        await api.translate("Kamisato Ayaka")
