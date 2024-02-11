from dataclasses import dataclass
from enum import Enum
from async_github.models.model import Model


class OwnerType(Enum):
    USER = "User"
    ORGANIZATION = "Organization"

    def __repr__(self):
        return self.value


@dataclass(init=False)
class Owner(Model):
    login: str
    id: int
    type: OwnerType
    site_admin: bool
    node_id: str

    def __post_init__(self):
        # Convert to enum
        self.type = OwnerType(self.type)
