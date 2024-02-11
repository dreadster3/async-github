from collections.abc import Callable
from typing import Generic, Literal, TypeVar, Union


T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class Ok(Generic[T, E]):
    __match_args__ = ("value",)

    def __init__(self, value: T):
        self.value = value

    def is_ok(self) -> Literal[True]:
        return True

    def is_err(self) -> Literal[False]:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_err(self) -> E:
        raise ValueError("Cannot unwrap error from Ok")

    def unwrap_or(self, default: T) -> T:
        return self.value

    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        return self.value

    def __repr__(self) -> str:
        return f"Ok({self.value})"


class Err(Generic[T, E]):
    __match_args__ = ("error",)

    def __init__(self, error: E):
        self.error = error

    def is_ok(self) -> Literal[False]:
        return False

    def is_err(self) -> Literal[True]:
        return True

    def unwrap(self) -> T:
        raise self.error

    def unwrap_err(self) -> E:
        return self.error

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        return f(self.error)

    def __repr__(self) -> str:
        return f"Err({self.error})"


Result = Union[Ok[T, E], Err[T, E]]
