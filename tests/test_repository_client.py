import pytest

from async_github.clients.repository_client import RepositoryClient


@pytest.mark.asyncio
async def test_get_repository_async():
    async with RepositoryClient("dreadster3", "async_github") as client:
        response = await client.get_repository_async()

        assert response is not None
        assert response.name == "async_github"
        assert response.owner.login == "dreadster3"


@pytest.mark.asyncio
async def test_cache_async():
    import datetime

    async with RepositoryClient("dreadster3", "async_github") as client:

        start_time = datetime.datetime.now()
        response = await client.get_repository_async()
        end_time = datetime.datetime.now()

        request_time = end_time - start_time

        assert response is not None
        assert response.name == "async_github"
        assert response.owner.login == "dreadster3"

        start_time = datetime.datetime.now()
        response = await client.get_repository_async()
        end_time = datetime.datetime.now()

        assert response is not None
        assert response.name == "async_github"
        assert response.owner.login == "dreadster3"

        assert request_time > (end_time - start_time)
