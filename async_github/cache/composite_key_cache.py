import cachetools
from typing import Any, List, Optional, Union


class CompositeKeyCache:
    KeyType = Union[str, List[str]]

    def __init__(self, cache: cachetools.Cache = cachetools.LRUCache(maxsize=100)) -> None:
        self._cache = cache

    def __setitem__(self, key: KeyType, value: Any) -> None:
        self.add(key, value)

    def __getitem__(self, key: KeyType) -> Optional[Any]:
        return self.get(key) or self.get_children(key)

    @property
    def size(self) -> int:
        return int(self._cache.currsize)

    def add(self, key: KeyType, value: Any) -> None:
        if isinstance(key, str):
            key = [key]

        key = ".".join(key)

        self._cache[key] = value

    def get(self, key: KeyType) -> Optional[Any]:
        if isinstance(key, str):
            key = [key]

        key = ".".join(key)
        self._cache.update

        return self._cache.get(key)

    def get_children(self, key: KeyType) -> Optional[List[Any]]:
        if isinstance(key, str):
            key = [key]

        key = ".".join(key)

        result = []
        for k in self._cache.keys():
            if k.startswith(key) and k != key:
                result.append(self._cache.get(k))

        if result:
            return result

        return None

    def remove(self, key: KeyType) -> None:
        if isinstance(key, str):
            key = [key]

        key = ".".join(key)

        self._cache.pop(key)

    def remove_match(self, key: KeyType) -> None:
        if isinstance(key, str):
            key = [key]

        key = ".".join(key)

        keys = list(self._cache.keys())
        for k in keys:
            if k.startswith(key):
                self._cache.pop(k)
