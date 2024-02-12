import asyncio
from aiohttp import ClientResponseError, ClientSession, ClientTimeout
from uuid import uuid4, UUID
from typing import Dict, Optional
from enum import Enum

from async_github.helpers import Result, Err, Ok
from async_github.logs import ContextLogger
from async_github.models import HttpResponse


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class AsyncHttpClient:
    ResponseType = Result[HttpResponse, ClientResponseError]

    def __init__(self, base_url: Optional[str] = None, headers: Dict[str, str] = {}, session: Optional[ClientSession] = None, timeout: Optional[ClientTimeout] = None):
        timeout = timeout or ClientTimeout(total=2*60, connect=60)

        self._header_mask = {
            "Authorization": False
        }

        self._session_id: UUID = uuid4()
        self._session: ClientSession = session or ClientSession(
            base_url=base_url, timeout=timeout, headers=headers)
        self._logger = ContextLogger(self.__class__.__name__, {
            "session_id": self._session_id
        })

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def __aenter__(self):
        return self

    # def __del__(self):
    #     if self._session and asyncio.get_running_loop():
    #         asyncio.create_task(self.close())

    def is_closed(self) -> bool:
        """Check if the session is closed

        Returns:
            bool: True if the session is closed, False otherwise
        """
        return self._session.closed

    def is_open(self) -> bool:
        """Check if the session is open

        Returns:
            bool: True if the session is open, False otherwise
        """
        return not self.is_closed()

    async def close(self):
        """Close the session if it is open"""
        if self._session and not self._session.closed:
            self._logger.debug("Closing session %s", self._session_id)
            await self._session.close()

    async def _request(self, method: HTTPMethod, url: str, data: Optional[dict] = None, headers: Optional[Dict[str, str]] = {}, params: Dict[str, str] = {}) -> ResponseType:
        """Make a HTTP request to the given url

        Args:
            method: Method to use for the request
            url: URL to make the request to
            data: Data to send with the request
            headers: Headers to send with the request
            params: Query parameters to send with the request

        Returns:
            HttpResponse: Response from the server
        """
        # If the url does not start with http or /, then it is a relative url
        url = url if url.startswith(
            "http") or url.startswith("/") else f"/{url}"

        request_id = uuid4()
        self._logger.add_context(
            {"request_id": request_id, "method": method.value, "url": url})

        self._logger.info(
            "%s to %s [%s]", method.value, url, request_id)
        start_time = asyncio.get_event_loop().time()
        try:
            async with self._session.request(method.value, url, data=data, headers=headers, params=params) as response:
                response.raise_for_status()
                end_time = asyncio.get_event_loop().time()
                self._logger.info("Request completed in %sms with status %s [%s]",
                                  (end_time - start_time) * 1000, response.status, request_id)
                json = await response.json()
                return Ok(HttpResponse(response.status, dict(response.headers), json))
        except ClientResponseError as error:
            end_time = asyncio.get_event_loop().time()
            self._logger.info(
                "Request completed in %sms with status %s [%s]", (end_time - start_time) * 1000, error.status, request_id)
            return Err(error)

    async def _get_async(self, url: str, headers: Optional[Dict[str, str]] = {}, params: Dict[str, str] = {}) -> ResponseType:
        """Make a GET request to the given url

        Args:
            url: URL to make the request to
            headers: Headers to send with the request
            params: Query parameters to send with the request

        Returns:
            HttpResponse: Response from the server
        """
        return await self._request(HTTPMethod.GET, url, headers=headers, params=params)

    async def _post_async(self, url: str, data: Optional[dict] = None, headers: Optional[Dict[str, str]] = {}, params: Dict[str, str] = {}) -> ResponseType:
        """Make a POST request to the given url

        Args:
            url: URL to make the request to
            data: Data to send with the request
            headers: Headers to send with the request
            params: Query parameters to send with the request

        Returns:
            HttpResponse: Response from the server
        """
        return await self._request(HTTPMethod.POST, url, data=data, headers=headers, params=params)

    async def _put_async(self, url: str, data: Optional[dict] = None, headers: Optional[Dict[str, str]] = {}, params: Dict[str, str] = {}) -> ResponseType:
        """Make a PUT request to the given url

        Args:
            url: URL to make the request to
            data: Data to send with the request
            headers: Headers to send with the request
            params: Query parameters to send with the request

        Returns:
            HttpResponse: Response from the server
        """
        return await self._request(HTTPMethod.PUT, url, data=data, headers=headers, params=params)

    async def _delete_async(self, url: str, headers: Optional[Dict[str, str]] = {}, params: Dict[str, str] = {}) -> ResponseType:
        """Make a DELETE request to the given url

        Args:
            url: URL to make the request to
            headers: Headers to send with the request
            params: Query parameters to send with the request

        Returns:
            HttpResponse: Response from the server
        """
        return await self._request(HTTPMethod.DELETE, url, headers=headers, params=params)

    async def _patch_async(self, url: str, data: Optional[dict] = None, headers: Optional[Dict[str, str]] = {}, params: Dict[str, str] = {}) -> ResponseType:
        """Make a PATCH request to the given url

        Args:
            url: URL to make the request to
            data: Data to send with the request
            headers: Headers to send with the request
            params: Query parameters to send with the request

        Returns:
            HttpResponse: Response from the server
        """
        return await self._request(HTTPMethod.PATCH, url, data=data, headers=headers, params=params)

    async def _options_async(self, url: str, headers: Optional[Dict[str, str]] = {}, params: Dict[str, str] = {}) -> ResponseType:
        """Make a OPTIONS request to the given url

        Args:
            url: URL to make the request to
            headers: Headers to send with the request
            params: Query parameters to send with the request

        Returns:
            HttpResponse: Response from the server
        """
        return await self._request(HTTPMethod.OPTIONS, url, headers=headers, params=params)

    async def _head_async(self, url: str, headers: Optional[Dict[str, str]] = {}, params: Dict[str, str] = {}) -> ResponseType:
        """Make a HEAD request to the given url

        Args:
            url: URL to make the request to
            headers: Headers to send with the request
            params: Query parameters to send with the request

        Returns:
            HttpResponse: Response from the server
        """
        return await self._request(HTTPMethod.HEAD, url, headers=headers, params=params)
