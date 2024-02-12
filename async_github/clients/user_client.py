from aiohttp import ClientSession
from async_github.clients import RepositoryClient
from async_github.helpers import Err, Ok
from async_github.models import Repository, User
from typing import List, Optional
from async_github.clients.base_github_client import BaseGithubClient


class UserClient(BaseGithubClient):
    def __init__(self, username: str, token: Optional[str] = None, session: Optional[ClientSession] = None):
        self.username = username
        super().__init__(token, session)

    def get_repository_client(self, repository_name: str) -> RepositoryClient:
        return RepositoryClient(self.username, repository_name, self._token, self._session)

    async def get_user_async(self) -> Optional[User]:
        if user := self._cache[["users", self.username]]:
            return user

        result = await self._get_async(f"/users/{self.username}")

        match result:
            case Ok(response):
                user = User(**response.body)
                self._cache[["users", self.username]] = user
                return user
            case Err(err):
                if err.status == 404:
                    return None
                raise err

    async def get_user_repositories_async(self) -> List[Repository]:
        if repositories := self._cache[[self.username, "repository"]]:
            return repositories

        result = await self._get_async(f"/users/{self.username}/repos")

        response = result.unwrap()

        repositories = list(
            map(lambda repo: Repository(**repo), response.body))
        self._cache[[self.username, "repository"]] = repositories

        return repositories
