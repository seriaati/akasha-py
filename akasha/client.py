from typing import Any, Final, Self

from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession
from loguru import logger

from akasha.models.leaderboard import LeaderboardPaginator

from .enums import Language
from .errors import DESC_TO_ERROR, AkashaAPIError
from .models import Leaderboard, UserCalc
from .models.artifact import Artifact

__all__ = ("AkashaAPI",)


class AkashaAPI:
    BASE_URL: Final[str] = "https://akasha.cv/api"

    def __init__(
        self,
        lang: Language = Language.ENGLISH,
        headers: dict[str, Any] | None = None,
        cache_name: str = "./.cache/akasha-py.db",
        cache_ttl: int = 360,
        debug: bool = False,
    ) -> None:
        self._lang = lang
        self._headers = headers or {"User-Agent": "akasha-py"}
        self._cache_name = cache_name
        self._cache_ttl = cache_ttl
        self._session: CachedSession | None = None
        self.debug = debug

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        await self.close()

    async def start(self) -> None:
        cache = SQLiteBackend(self._cache_name, expire_after=self._cache_ttl)
        self._session = CachedSession(cache=cache)

    async def close(self) -> None:
        if self._session is None:
            return
        await self._session.close()

    def _raise_for_error(self, data: list[dict[str, Any]] | dict[str, Any]) -> None:
        if isinstance(data, list):
            return

        if (error := data.get("error")) is not None:
            if (message := data.get("message")) is not None:
                title = message
                description = error
            else:
                title = error["title"]
                description = error["description"]

            if (error_class := DESC_TO_ERROR.get(description)) is not None:
                raise error_class(title, description)
            raise AkashaAPIError(title, description)

    async def _request(
        self, endpoint: str, use_cache: bool, *, params: dict[str, Any] | None = None
    ) -> Any:
        if self._session is None:
            msg = f"Session is not started, call {self.__class__.__name__}.start() first."
            raise RuntimeError(msg)

        url = f"{self.BASE_URL}/{endpoint}"
        params = params or {}
        if self.debug:
            logger.debug(f"Requesting {url} with params {params}")

        if not use_cache:
            async with self._session.disabled(), self._session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
        else:
            async with self._session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()

        data = data.get("data", data)
        self._raise_for_error(data)
        return data

    async def get_calculations_for_user(
        self, uid: int, *, use_cache: bool = True
    ) -> list[UserCalc]:
        """Get the calculations for a user.

        Args:
            uid: The user ID.
            use_cache: Whether to use the cache.
        """
        data = await self._request(f"getCalculationsForUser/{uid}", use_cache=use_cache)
        user_calcs = [UserCalc(**calc) for calc in data]

        strings: set[str] = set()
        for user_calc in user_calcs:
            strings.add(user_calc.name)
            for calc in user_calc.calculations:
                strings.add(calc.weapon.name)

        translations = await self.get_translations(list(strings))

        for user_calc in user_calcs:
            user_calc.name = translations.get(user_calc.name.lower(), user_calc.name)
            for calc in user_calc.calculations:
                calc.weapon.name = translations.get(calc.weapon.name.lower(), calc.weapon.name)

        return user_calcs

    async def _fetch_leaderboards(
        self, calculation_id: int, page: int, page_size: int, p: str, use_cache: bool
    ) -> list[Leaderboard]:
        data = await self._request(
            "leaderboards",
            params={
                "calculationId": calculation_id,
                "size": page_size,
                "page": page,
                "sort": "calculation.result",
                "order": -1,
                "p": p,
            },
            use_cache=use_cache,
        )
        return [Leaderboard(**lb) for lb in data]

    def get_leaderboards(
        self, calculation_id: int, max_page: int, *, page_size: int = 20, use_cache: bool = True
    ) -> LeaderboardPaginator:
        """Get a leaderboard paginator for a calculation.

        Args:
            calculation_id: The calculation ID.
            max_page: The maximum number of pages to return.
            page_size: The number of leaderboards to return per page.
            use_cache: Whether to use the cache.
        """
        return LeaderboardPaginator(
            self._fetch_leaderboards, calculation_id, page_size, max_page, use_cache
        )

    async def refresh_user(self, uid: int) -> None:
        """Refresh the Enka data of a player.

        Args:
            uid: The UID of the player.
        """
        await self._request(f"user/refresh/{uid}", use_cache=False)

    async def get_user(self, uid: int, *, use_cache: bool = True) -> None:
        """Get the user data.

        Args:
            uid: The UID of the player.
            use_cache: Whether to use the cache.
        """
        msg = "This method is not implemented yet."
        raise NotImplementedError(msg)
        await self._request(f"user/{uid}", use_cache=use_cache)

    async def get_translations(self, words: list[str], *, use_cache: bool = True) -> dict[str, str]:
        """Get the translations for a list of words.

        Args:
            words: The list of words to translate.
            use_cache: Whether to use the cache.

        Returns:
            A dictionary of the translations. Key is word.lower(), value is the translation.
        """
        if self._lang is Language.ENGLISH:
            return {word.lower(): word for word in words}

        data = await self._request(
            f"textmap/{self._lang.value}", use_cache=use_cache, params={"words[]": words}
        )
        return data["translation"]

    async def translate(self, word: str) -> str:
        """Translate a word.

        Do not use this method for multiple translations, use get_translations instead.

        Args:
            word: The word to translate.

        Returns:
            The translation of the word.
        """
        if self._lang is Language.ENGLISH:
            return word

        return (await self.get_translations([word]))[word.lower()]

    async def get_artifacts(self, uid: int, md5: str, *, use_cache: bool = True) -> list[Artifact]:
        """Get the artifacts of a build.

        Args:
            uid: The UID of the owner of the build.
            md5: The MD5 hash of the build.
            use_cache: Whether to use the cache.
        """
        data = await self._request(f"artifacts/{uid}/{md5}", use_cache=use_cache)
        return [Artifact(**artifact) for artifact in data]
