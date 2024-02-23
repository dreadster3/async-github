import pytest
from python_query import query_cache

from async_github.clients.base_github_client import BaseGithubClient
from async_github.clients.repository_client import RepositoryClient


@pytest.mark.asyncio
async def test_get_repository_async() -> None:
    async with RepositoryClient("dreadster3", "async-github") as client:
        test_cache = query_cache.QueryCache()
        client._cache = test_cache
        response = await client.get_repository_async()

        assert response is not None
        assert response.name == "async-github"
        assert response.owner.login == "dreadster3"


@pytest.mark.asyncio
async def test_cache_async() -> None:
    owner = "dreadster3"
    repository_name = "async-github"

    async with RepositoryClient(owner, repository_name) as client:
        test_cache = query_cache.QueryCache()
        client._cache = test_cache

        assert test_cache.get_query(
            [owner, "repository", repository_name]) is None

        response = await client.get_repository_async()

        assert response is not None
        assert response.name == "async-github"
        assert response.owner.login == "dreadster3"
        assert test_cache.get_query(
            [owner, "repository", repository_name]) is not None

        response2 = await client.get_repository_async()

        assert response2 is not None
        assert response2 == response
        assert test_cache.get_query(
            [owner, "repository", repository_name]) is not None
