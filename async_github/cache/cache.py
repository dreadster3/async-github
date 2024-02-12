from __future__ import annotations
import logging
from typing import Any, List, Optional, Union
from datetime import datetime


class CacheEntry:
    def __init__(self, key: str, value: Any, parent: Optional[CacheEntry] = None, children: Optional[List[CacheEntry]] = None):
        self.key = key
        self.value = value
        self.parent = parent
        self.children = children or []
        self.last_accessed = datetime.now()

    def _update_last_accessed(self):
        self.last_accessed = datetime.now()

    def _sort_children(self):
        self.children.sort(key=lambda c: c.last_accessed)

    def set_value(self, value: Any) -> CacheEntry:
        self._update_last_accessed()
        self.value = value
        return self

    def set_child(self, key: str, value: Any) -> CacheEntry:
        self._update_last_accessed()
        if key in self.get_children_keys():
            entry = next(c for c in self.children if c.key == key)
            return entry.set_value(value)

        return self.add_child(key, value)

    def add_child(self, key: str, value: Any) -> CacheEntry:
        self._update_last_accessed()
        child = CacheEntry(key, value, self)
        self.children.append(child)
        return child

    def remove_child(self, child: CacheEntry):
        self._update_last_accessed()
        self.children.remove(child)

    def get_children_keys(self) -> List[str]:
        return [c.key for c in self.children]

    def get_oldest_child(self) -> CacheEntry:
        self._sort_children()
        return self.children[0]

    @property
    def size(self) -> int:
        if not self.children or len(self.children) == 0:
            return self.value != None

        return 1 + sum(c.size for c in self.children)

    def __repr__(self) -> str:
        if not self.children or len(self.children) == 0:
            return f"CacheEntry({self.key}, {self.value})"

        return f"CacheEntry({self.key}, {self.value}, Children: ({self.children}))"


class Cache:
    KeyType = Union[str, List[str]]

    def __init__(self):
        self._root = CacheEntry("root", None)
        self._max_size = 100
        self._logger = logging.getLogger(self.__class__.__name__)

    def _remove_oldest_child(self, root: CacheEntry) -> None:
        self._logger.debug(f"Removing oldest child from {root.key}")
        if not root.children or len(root.children) == 0:
            if root.parent:
                root.parent.remove_child(root)
            return

        oldest = root.get_oldest_child()
        return self._remove_oldest_child(oldest)

    def _add_cache_entry(self, root: CacheEntry, key: List[str], value: Any) -> CacheEntry:
        if len(key) == 1:
            return root.set_child(key[0], value)

        current = key[0]
        if current not in root.get_children_keys():
            root.add_child(current, None)

        return self._add_cache_entry(next(c for c in root.children if c.key == current), key[1:], value)

    def add_cache_entry(self, key: KeyType, value: Any) -> CacheEntry:
        if isinstance(key, str):
            key = [key]

        entry = self._add_cache_entry(self._root, key, value)
        self._logger.debug(f"Set cache entry {key} with value {value}")

        while self.size > self._max_size:
            self._logger.debug(
                f"Cache size has exceeded maximum size of {self._max_size}")
            self._remove_oldest_child(self._root)

        return entry

    def _get_cache_entry(self, root: CacheEntry, key: List[str]) -> Optional[CacheEntry]:
        if len(key) == 1:
            return next((c for c in root.children if c.key == key[0]), None)

        current = key[0]
        if current not in root.get_children_keys():
            return None

        return self._get_cache_entry(next(c for c in root.children if c.key == current), key[1:])

    def get_cache_value(self, key: KeyType) -> Any:
        if isinstance(key, str):
            key = [key]

        return self._get_cache_entry(self._root, key).value

    @ property
    def size(self) -> int:
        # Subtract 1 because the root node is not a cache entry
        return self._root.size - 1

    def view_data(self):
        return str(self._root.children)
