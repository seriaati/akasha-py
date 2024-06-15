from typing import Any, Final, Self

from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession

from akasha.models.leaderboard import Leaderboard

from .models import UserCalc

__all__ = ("AkashaAPI",)


class AkashaAPI:
    BASE_URL: Final[str] = "https://akasha.cv/api"

    def __init__(
        self,
        headers: dict[str, Any] | None = None,
        cache_name: str = "./.cache/akasha-py.db",
        cache_ttl: int = 360,
    ) -> None:
        self._headers = headers or {"User-Agent": "akasha-py"}
        self._cache_name = cache_name
        self._cache_ttl = cache_ttl
        self._session: CachedSession | None = None

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

    async def _request(
        self, endpoint: str, use_cache: bool, *, params: dict[str, Any] | None = None
    ) -> Any:
        if self._session is None:
            msg = f"Session is not started, call {self.__class__.__name__}.start() first."
            raise RuntimeError(msg)

        url = f"{self.BASE_URL}/{endpoint}"
        params = params or {}

        if not use_cache:
            async with self._session.disabled(), self._session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
        else:
            async with self._session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()

        return data["data"]

    async def get_calculations_for_user(
        self, uid: int, *, use_cache: bool = True
    ) -> list[UserCalc]:
        """Get the calculations for a user.

        Args:
            uid (int): The user ID.
            use_cache (bool): Whether to use the cache.
        """
        data = await self._request(f"getCalculationsForUser/{uid}", use_cache=use_cache)
        return [UserCalc(**calc) for calc in data]

    async def get_leaderboards(
        self, calculation_id: int, *, size: int = 10, page: int = 1, use_cache: bool = True
    ) -> list[Leaderboard]:
        """Get the leaderboards for a calculation.

        Args:
            calculation_id (int): The calculation ID.
            size (int): The number of leaderboards to return.
            page (int): The page number.
            use_cache (bool): Whether to use the cache.
        """
        data = await self._request(
            "leaderboards",
            params={
                "calculationId": calculation_id,
                "size": size,
                "page": page,
                "sort": "calculation.result",
                "order": -1,
            },
            use_cache=use_cache,
        )
        return [Leaderboard(**lb) for lb in data]
