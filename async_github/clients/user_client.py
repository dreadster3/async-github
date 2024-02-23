from typing import List, Optional

from aiohttp import ClientSession
from python_query import QueryCache

from async_github.clients import RepositoryClient
from async_github.clients.base_github_client import BaseGithubClient
from async_github.helpers import Err, Ok
from async_github.models import Repository, User
from async_github.models.page_params import PageParams


class UserClient(BaseGithubClient):
    def __init__(
            self,
            username: str,
            token: Optional[str] = None,
            session: Optional[ClientSession] = None):
        self.username = username
        super().__init__(token, session)

    def get_repository_client(
            self, repository_name: str) -> RepositoryClient:
        """Get a repository client

        Args:
            repository_name: Repository name

        Returns:
            RepositoryClient: Repository client
        """

        return RepositoryClient(
            self.username,
            repository_name,
            self._token,
            self._session)

    @QueryCache.cache(lambda self: self._cache,
                      lambda self: ["users", self.username])
    async def get_user_async(self) -> Optional[User]:
        """Get a user by username

        Returns:
            Optional[User]: User object if found, None otherwise
        """
        result = await self._get_async(f"/users/{self.username}")

        match result:
            case Ok(response):
                return User(**response.body)
            case Err(err):
                if err.status == 404:
                    return None
                raise err

    @QueryCache.cache(lambda self: self._cache, lambda self: [
                      self.username, "repository"])
    async def get_user_repositories_async(self,
                                          params: PageParams = PageParams()) -> List[Repository]:
        """Get the repositories of a user

        Returns:
            List[Repository]: List of repositories
        """

        result = await self._get_async(f"/users/{self.username}/repos", params=params.get_params())

        response = result.unwrap()

        return list(map(lambda repo: Repository(**repo), response.body))
