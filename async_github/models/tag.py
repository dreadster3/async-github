from dataclasses import dataclass
from async_github.models import Commit
from async_github.models.model import Model


@dataclass(init=False)
class Tag(Model):
    name: str
    commit: Commit
    zipball_url: str
    tarball_url: str
    node_id: str

    def __post_init__(self):
        if isinstance(self.commit, dict):
            self.commit = Commit(**self.commit)
