from async_github.helpers import Err, Ok
from async_github.models import Repository, User
from typing import List, Optional
from async_github.clients.base_github_client import BaseGithubClient


class UserClient(BaseGithubClient):
    def __init__(self, username: str, token: Optional[str] = None):
        self.username = username
        super().__init__(token)

    async def get_user_async(self) -> Optional[User]:
        result = await self._get_async(f"/users/{self.username}")

        match result:
            case Ok(response):
                return User(**response.body)
            case Err(err):
                if err.status == 404:
                    return None
                raise err

    async def get_user_repositories_async(self) -> List[Repository]:
        result = await self._get_async(f"/users/{self.username}/repos")

        response = result.unwrap()

        return list(map(lambda repo: Repository(**repo), response.body))
