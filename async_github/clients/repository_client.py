from typing import List, Optional
from async_github.clients.base_github_client import BaseGithubClient
from async_github.helpers.result import Err, Ok
from async_github.models import Repository, Tag
from async_github.models.page_params import PageParams


class RepositoryClient(BaseGithubClient):
    def __init__(self, owner: str, repository_name: str, token: Optional[str] = None):
        self.owner = owner
        self.repository_name = repository_name
        super().__init__(token)

    async def get_repository_async(self, params: PageParams = PageParams()) -> Optional[Repository]:
        """Get a repository by owner and repository name

        Args:
            params: PageParams pagination parameters

        Returns:
            Optional[Repository]: Repository object if found, None otherwise
        """
        result = await self._get_async(f"/repos/{self.owner}/{self.repository_name}", params=params.get_params())

        match result:
            case Ok(response):
                return Repository(**response.body)
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
        result = await self._get_async(f"/repos/{self.owner}/{self.repository_name}/tags", params=params.get_params())

        match result:
            case Ok(response):
                return list(map(lambda tag: Tag(**tag), response.body))
            case Err(err):
                raise err
