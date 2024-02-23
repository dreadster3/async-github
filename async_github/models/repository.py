from dataclasses import dataclass
from enum import Enum
from typing import List

from async_github.models.model import Model
from async_github.models.owner import Owner


class RepositoryVisibility(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"

    def __repr__(self) -> str:
        return self.value


@dataclass(init=False)
class Repository(Model):
    id: int
    node_id: str
    name: str
    full_name: str
    owner: Owner
    private: bool
    description: str
    fork: bool
    url: str
    forks_count: int
    stargazers_count: int
    watchers_count: int
    size: int
    default_branch: str
    open_issues_count: int
    is_template: bool
    topics: List[str]
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    has_downloads: bool
    archived: bool
    disabled: bool
    visibility: RepositoryVisibility

    def __post_init__(self) -> None:
        # Convert to model
        self.visibility = RepositoryVisibility(self.visibility)
        if isinstance(self.owner, dict):
            self.owner = Owner(**self.owner)
