import pytest

from async_github.clients.async_http_client import AsyncHttpClient


@pytest.mark.asyncio
async def test_get_async_http_client():
    async with AsyncHttpClient("https://api.github.com") as client:
        response = await client._get_async("/users/dreadster3")

        assert response is not None
        assert response.is_ok()
