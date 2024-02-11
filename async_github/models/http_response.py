from typing import Any, Dict


class HttpResponse:
    def __init__(self, status_code: int, headers: Dict[str, str], body: Any):
        self.status_code: int = status_code
        self.headers: Dict[str, str] = headers
        self.body: Any = body

    def is_ok(self):
        return 200 <= self.status_code < 300
