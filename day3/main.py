from dataclasses import dataclass
from pathlib import Path
from typing import List, Set

from utils.utils import flatten

NON_SYMBOLS = {"."}.union({str(i) for i in range(10)})


@dataclass
class NumberAndCoordinate:
    number: int
    x: int
    y: int

    @classmethod
    def parse_from_row(cls, row: str, y: int) -> List["NumberAndCoordinate"]:
        numbers_and_coordinates = []
        i = 0
        while i < len(row):
            c = row[i]
            if not c.isdigit():
                i += 1
                continue
            number = ""
            x = i
            while c.isdigit():
                number += c
                i += 1
                if i >= len(row):
                    break
                c = row[i]
            numbers_and_coordinates.append(
                NumberAndCoordinate(number=int(number), x=x, y=y)
            )

        return numbers_and_coordinates


def get_adjacent_symbols(
    schematic: List[str], number_and_coordinate: NumberAndCoordinate
) -> Set[str]:
    x_start = max(number_and_coordinate.x - 1, 0)
    x_end = min(
        number_and_coordinate.x + len(str(number_and_coordinate.number)),
        len(schematic[0]) - 1,
    )
    y_start = max(number_and_coordinate.y - 1, 0)
    y_end = min(number_and_coordinate.y + 1, len(schematic) - 1)

    symbols = set()
    for x in range(x_start, x_end + 1):
        for y in range(y_start, y_end + 1):
            if y == number_and_coordinate.y and (
                number_and_coordinate.x
                <= x
                <= number_and_coordinate.x + len(str(number_and_coordinate.number)) - 1
            ):
                continue
            symbols.add(schematic[y][x])

    return symbols


def is_part_number(
    schematic: List[str], number_and_coordinate: NumberAndCoordinate
) -> bool:
    return (
        len(
            get_adjacent_symbols(schematic, number_and_coordinate).difference(
                NON_SYMBOLS
            )
        )
        > 0
    )


def main() -> None:
    schematic = Path("input/input.txt").read_text("utf-8").split("\n")
    numbers_and_coordinates = flatten(
        [NumberAndCoordinate.parse_from_row(row, y) for y, row in enumerate(schematic)]
    )
    part_numbers = [
        number_and_coordinate
        for number_and_coordinate in numbers_and_coordinates
        if is_part_number(schematic, number_and_coordinate)
    ]
    print(sum(part_number.number for part_number in part_numbers))


if __name__ == "__main__":
    main()
