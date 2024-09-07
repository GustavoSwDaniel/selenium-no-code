from abc import ABC, abstractmethod
from typing import Dict

class IExecuteTesteUseCase(ABC):

    abstractmethod
    def execute(self) -> Dict: pass