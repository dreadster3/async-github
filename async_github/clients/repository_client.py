from typing import List, Optional
from aiohttp import ClientSession
from cachetools import cachedmethod

from async_github.clients.base_github_client import BaseGithubClient
from async_github.helpers.result import Err, Ok
from async_github.models import Repository, Tag
from async_github.models.page_params import PageParams


class RepositoryClient(BaseGithubClient):
    def __init__(self, owner: str, repository_name: str, token: Optional[str] = None, session: Optional[ClientSession] = None):
        self.owner = owner
        self.repository_name = repository_name
        super().__init__(token, session)

    async def get_repository_async(self) -> Optional[Repository]:
        """Get a repository by owner and repository name

        Args:
            params: PageParams pagination parameters

        Returns:
            Optional[Repository]: Repository object if found, None otherwise
        """

        # Check if the repository is in the cache
        if repository := self._cache[[self.owner, "repository", self.repository_name]]:
            return repository

        # Check if the repository is in the cache as a child
        if children := self._cache.get_children([self.owner, "repository"]):
            for child in children:
                if child.name == self.repository_name:
                    return child

        result = await self._get_async(f"/repos/{self.owner}/{self.repository_name}")

        match result:
            case Ok(response):
                repository = Repository(**response.body)
                self._cache[[self.owner, "repository",
                             self.repository_name]] = repository
                return repository
            case Err(err):
                if err.status == 404:
                    return None
                raise err

    async def get_repository_tags_async(self, params: PageParams = PageParams()) -> List[Tag]:
        """Get the tags of a repository

        Args:
            params: PageParams pagination parameters

        Returns:
            List[Tag]: List of tags
        """
        if tags := self._cache[["repository", self.owner, self.repository_name, "tags"]]:
            return tags

        result = await self._get_async(f"/repos/{self.owner}/{self.repository_name}/tags", params=params.get_params())

        match result:
            case Ok(response):
                tags = list(map(lambda tag: Tag(**tag), response.body))
                self._cache[["repository", self.owner,
                             self.repository_name, "tags"]] = tags
                return tags
            case Err(err):
                raise err
