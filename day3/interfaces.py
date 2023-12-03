from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, Type

from utils.utils import T, X


@dataclass(frozen=True)
class IValueAndCoordinate(ABC, Generic[T]):
    value: T
    x: int
    y: int
    length: int

    @classmethod
    @abstractmethod
    def try_parse_from_schematic(
        cls: Type[X], schematic: List[str], x: int, y: int
    ) -> Optional[X]:
        """
        :param schematic: The schematic "map" from which to parse the ValueAndCoordinate
        :param x: The x coordinate of the Value that should be parsed
        :param y: The y coordinate of the Value that should be parsed
        :return: If the x,y coordinate is part of a Value that can be parsed, return the parsed
        ValueAndCoordinate. Otherwise, returns None.
        """
