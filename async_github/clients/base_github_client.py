from os import environ
from typing import Optional
from aiohttp import ClientSession

from cachetools import LRUCache
from async_github.cache import CompositeKeyCache
from async_github.clients.async_http_client import AsyncHttpClient


class BaseGithubClient(AsyncHttpClient):
    _cache = CompositeKeyCache(LRUCache(100))

    def __init__(self, token: Optional[str] = None, session: Optional[ClientSession] = None):
        base_url = "https://api.github.com"
        self._token = token or environ.get("GITHUB_TOKEN", "")
        defautl_headers = {
            "Accept": "application/vnd.github.v3+json",
        }

        if token:
            defautl_headers["Authorization"] = f"Bearer {token}"

        super().__init__(base_url, defautl_headers, session)
