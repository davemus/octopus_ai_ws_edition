from abc import ABC, abstractmethod
from typing import Dict, Any


class Model(ABC):

    @abstractmethod
    def predict(self, data: Dict[str, Any]) -> float:
        raise NotImplementedError()

    @abstractmethod
    def load(self):
        raise NotImplementedError()
