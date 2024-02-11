from collections.abc import Mapping
import logging
from typing import Any, Dict, List


class ContextLogger:
    def __init__(self, name: str, context: Dict[str, Any] = {}):
        self.__context = context
        self.__logger = logging.getLogger(name)

    def set_context(self, context: Dict[str, Any]):
        self.__context = context

    def get_context(self) -> Dict[str, Any]:
        return self.__context

    def clear_context(self):
        self.__context.clear()

    def add_context(self, context: Dict[str, Any]):
        self.__context.update(context)

    def remove_context(self, *keys: str):
        for key in keys:
            self.__context.pop(key, None)

    def log(
        self,
        level: int,
        msg: object,
        *args: object,
        exc_info: Any = None,
        extra: Dict[str, object] | None = None,
        stack_info: bool = False,
        stacklevel: int = 1,
    ) -> None:
        self._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

    def _log(
        self,
        level: int,
        msg: object,
        args: Any,
        exc_info: Any = None,
        extra: Dict[str, object] | None = None,
        stack_info: bool = False,
        stacklevel: int = 1,
    ) -> None:
        if extra is None:
            extra = {}

        extra.update(self.__context)
        self.__logger._log(level=level, msg=msg, args=args, extra=extra,
                           exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel)

    def debug(self, msg: object, *args: object) -> None:
        self.log(logging.DEBUG, msg, *args)

    def info(self, msg: object, *args: object) -> None:
        self.log(logging.INFO, msg, *args)

    def warning(self, msg: object, *args: object) -> None:
        self.log(logging.WARN, msg, *args)

    def error(self, msg: object, *args: object) -> None:
        self.log(logging.ERROR, msg, *args)
