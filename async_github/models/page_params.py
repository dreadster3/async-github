from async_github.models.params import Params


class PageParams(Params):
    def __init__(self, page: int = 1, page_size: int = 30):
        self.page = page
        self.page_size = page_size

    def get_params(self):
        return {
            "page": str(self.page),
            "per_page": str(self.page_size),
        }
