from abc import ABC, abstractmethod
from typing import Type

from utils.utils import T


class IParsable(ABC):
    @classmethod
    @abstractmethod
    def parse(cls: Type[T], string: str) -> T:
        """
        :param string: string that this class can be parsed from
        :return: an instance of the class parsed from the string
        """
