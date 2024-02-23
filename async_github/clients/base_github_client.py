from os import environ
from typing import Optional

from aiohttp.client import ClientSession
from python_query import QueryCache

from async_github.clients.async_http_client import AsyncHttpClient


class BaseGithubClient(AsyncHttpClient):
    _cache = QueryCache()

    def __init__(
            self,
            token: Optional[str] = None,
            session: Optional[ClientSession] = None) -> None:
        base_url = "https://api.github.com"
        self._token = token or environ.get("GITHUB_TOKEN", "")
        defautl_headers = {
            "Accept": "application/vnd.github.v3+json",
        }

        if token:
            defautl_headers["Authorization"] = f"Bearer {token}"

        super().__init__(base_url, defautl_headers, session)
