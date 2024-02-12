import logging
import asyncio
import sys

from cachetools import LRUCache, TTLCache
from async_github.cache.composite_key_cache import CompositeKeyCache
from async_github.clients import UserClient, BaseGithubClient
from async_github.clients.repository_client import RepositoryClient
from datetime import datetime


async def main():
    user_client = UserClient("dreadster3")

    repositories = await user_client.get_user_repositories_async()

    for r in repositories:
        repository_client = user_client.get_repository_client(r.name)
        tags = await repository_client.get_repository_tags_async()
        print("Tags for", r.name)
        print(tags)

    await user_client.close()


class ExtraArgsFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)


def setup_logger():
    formatter = ExtraArgsFormatter(
        fmt="%(asctime)s.%(msecs)03d [%(levelname).3s] %(process)s %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)


if __name__ == "__main__":
    setup_logger()
    logging.getLogger("async_github").info("Hello", extra={"test": "test"})
    asyncio.run(main())
