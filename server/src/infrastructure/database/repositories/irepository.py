from abc import ABCMeta, abstractmethod
from typing import Dict, List


class IRepository(metaclass=ABCMeta):
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory
    
    @abstractmethod
    def get_all(self) -> List: pass

    @abstractmethod
    async def filter_by(self, params: Dict): pass

    @abstractmethod
    async def filter_all_by(self, params: Dict): pass
