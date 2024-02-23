from abc import abstractmethod
from typing import Dict


class Params:
    @abstractmethod
    def get_params(self) -> Dict[str, str]:
        """Return the parameters to be used in the request.

        Returns:
            Dict[str, str]: The parameters to be used in the request.
        """
        raise NotImplementedError
