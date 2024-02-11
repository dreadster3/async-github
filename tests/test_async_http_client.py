import pytest

from async_github.clients.async_http_client import AsyncHttpClient


@pytest.mark.asyncio
async def test_get_async_http_client():
    client = AsyncHttpClient("https://api.github.com")

    response = await client.get("/users/dreadster3")

    assert response.is_ok()
