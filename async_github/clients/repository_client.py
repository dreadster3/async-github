from typing import List, Optional

from aiohttp import ClientSession
from python_query import QueryCache

from async_github.clients.base_github_client import BaseGithubClient
from async_github.helpers.result import Err, Ok
from async_github.models import PageParams, Repository, Tag


class RepositoryClient(BaseGithubClient):
    def __init__(
            self,
            owner: str,
            repository_name: str,
            token: Optional[str] = None,
            session: Optional[ClientSession] = None) -> None:
        self.owner = owner
        self.repository_name = repository_name
        super().__init__(token, session)

    @QueryCache.cache(lambda self: self._cache,
                      lambda self: [self.owner,
                                    "repository",
                                    self.repository_name])
    async def get_repository_async(self) -> Optional[Repository]:
        """Get a repository by owner and repository name

        Args:
            params: PageParams pagination parameters

        Returns:
            Optional[Repository]: Repository object if found, None otherwise
        """

        uri = f"/repos/{self.owner}/{self.repository_name}"
        result = await self._get_async(uri)

        match result:
            case Ok(response):
                return Repository(**response.body)
            case Err(err):
                raise err

    @QueryCache.cache(lambda self: self._cache,
                      lambda self: [self.owner,
                                    "repository",
                                    self.repository_name,
                                    "tags"])
    async def get_repository_tags_async(self, params: PageParams = PageParams()) -> List[Tag]:
        """Get the tags of a repository

        Args:
            params: PageParams pagination parameters

        Returns:
            List[Tag]: List of tags
        """
        result = await self._get_async(f"/repos/{self.owner}/{self.repository_name}/tags",
                                       params=params.get_params())

        match result:
            case Ok(response):
                tags = list(map(lambda tag: Tag(**tag), response.body))
                return tags
            case Err(err):
                raise err
