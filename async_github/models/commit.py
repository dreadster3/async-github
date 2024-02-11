from dataclasses import dataclass
from async_github.models.model import Model


@dataclass(init=False)
class Commit(Model):
    sha: str
    url: str
