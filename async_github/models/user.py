from dataclasses import dataclass
from async_github.models import Owner


@dataclass(init=False)
class User(Owner):
    name: str
    email: str
    bio: str
    company: str
    location: str
    blog: str
    hireable: bool
    twitter_username: str
    public_repos: int
    public_gists: int
    followers: int
    following: int
