import pytest

from async_github.clients.repository_client import RepositoryClient


@pytest.mark.asyncio
async def test_get_repository_async():
    async with RepositoryClient("dreadster3", "async_github") as client:
        response = await client.get_repository_async()

        assert response is not None
        assert response.name == "async_github"
        assert response.owner.login == "dreadster3"
