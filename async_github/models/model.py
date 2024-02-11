from dataclasses import dataclass


@dataclass(init=False)
class Model:
    def __init__(self, **kwargs):
        names = set([f for f in self.__dataclass_fields__.keys()])

        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)

        self.__post_init__()

    def __post_init__(self):
        pass
