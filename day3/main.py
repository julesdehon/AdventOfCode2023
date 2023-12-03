from math import prod
from pathlib import Path
from typing import List, Optional, Set, Type

from day3.interfaces import IValueAndCoordinate

NON_SYMBOLS = {"."}.union({str(i) for i in range(10)})


class SymbolAndCoordinate(IValueAndCoordinate):
    @classmethod
    def try_parse_from_schematic(
        cls, schematic: List[str], x: int, y: int
    ) -> Optional["SymbolAndCoordinate"]:
        value_at_coord = schematic[y][x]
        if value_at_coord in NON_SYMBOLS:
            return None

        return SymbolAndCoordinate(value=value_at_coord, x=x, y=y, length=1)


class NumberAndCoordinate(IValueAndCoordinate):
    @classmethod
    def try_parse_from_schematic(
        cls, schematic: List[str], x: int, y: int
    ) -> Optional["NumberAndCoordinate"]:
        if not schematic[y][x].isdigit():
            return None

        # Get first digit in number
        first_digit_x_coord = x
        coord_to_test = x - 1
        while coord_to_test >= 0 and schematic[y][coord_to_test].isdigit():
            first_digit_x_coord = coord_to_test
            coord_to_test -= 1

        # Get last digit in number
        last_digit_x_coord = first_digit_x_coord
        coord_to_test = last_digit_x_coord + 1
        while (
            coord_to_test < len(schematic[y]) and schematic[y][coord_to_test].isdigit()
        ):
            last_digit_x_coord = coord_to_test
            coord_to_test += 1

        return NumberAndCoordinate(
            value=int(schematic[y][first_digit_x_coord : last_digit_x_coord + 1]),
            x=first_digit_x_coord,
            y=y,
            length=last_digit_x_coord + 1 - first_digit_x_coord,
        )


def get_adjacent_values_of_type(
    schematic: List[str],
    value_and_coordinate: IValueAndCoordinate,
    type_to_find: Type[IValueAndCoordinate],
) -> Set[IValueAndCoordinate]:
    x_start = max(value_and_coordinate.x - 1, 0)
    x_end = min(
        value_and_coordinate.x + value_and_coordinate.length,
        len(schematic[0]) - 1,
    )
    y_start = max(value_and_coordinate.y - 1, 0)
    y_end = min(value_and_coordinate.y + 1, len(schematic) - 1)

    values = set()
    for x in range(x_start, x_end + 1):
        for y in range(y_start, y_end + 1):
            if y == value_and_coordinate.y and (
                value_and_coordinate.x
                <= x
                <= value_and_coordinate.x + value_and_coordinate.length - 1
            ):
                continue
            maybe_value = type_to_find.try_parse_from_schematic(
                schematic=schematic, x=x, y=y
            )
            if maybe_value is not None:
                values.add(maybe_value)

    return values


def is_part_number(
    schematic: List[str], number_and_coordinate: NumberAndCoordinate
) -> bool:
    return (
        len(
            get_adjacent_values_of_type(
                schematic, number_and_coordinate, SymbolAndCoordinate
            )
        )
        > 0
    )


def get_maybe_gear_ratio(
    schematic: List[str], symbol_and_coordinate: SymbolAndCoordinate
) -> Optional[int]:
    if symbol_and_coordinate.value != "*":
        return None
    adjacent_part_numbers = get_adjacent_values_of_type(
        schematic, symbol_and_coordinate, NumberAndCoordinate
    )
    if len(adjacent_part_numbers) != 2:
        return None

    return prod(
        adjacent_part_number.value for adjacent_part_number in adjacent_part_numbers
    )


def main() -> None:
    schematic = Path("input/input.txt").read_text("utf-8").split("\n")
    numbers_and_coordinates = set()
    symbols_and_coordinates = set()
    for y, row in enumerate(schematic):
        for x, _ in enumerate(row):
            maybe_number_and_coordinate = NumberAndCoordinate.try_parse_from_schematic(
                schematic, x, y
            )
            if maybe_number_and_coordinate is not None:
                numbers_and_coordinates.add(maybe_number_and_coordinate)
                continue

            maybe_symbol_and_coordinate = SymbolAndCoordinate.try_parse_from_schematic(
                schematic, x, y
            )
            if maybe_symbol_and_coordinate is not None:
                symbols_and_coordinates.add(maybe_symbol_and_coordinate)

    part_numbers = [
        number_and_coordinate
        for number_and_coordinate in numbers_and_coordinates
        if is_part_number(schematic, number_and_coordinate)
    ]
    print(f"The sum of all {len(part_numbers)} part numbers:")
    print(sum(part_number.value for part_number in part_numbers))

    gear_ratios = [
        maybe_gear_ratio
        for maybe_gear_ratio in [
            get_maybe_gear_ratio(schematic, symbol_and_coordinate)
            for symbol_and_coordinate in symbols_and_coordinates
        ]
        if maybe_gear_ratio is not None
    ]
    print(f"The sum of all {len(gear_ratios)} gear ratios:")
    print(sum(gear_ratio for gear_ratio in gear_ratios))


if __name__ == "__main__":
    main()
