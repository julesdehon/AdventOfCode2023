from __future__ import annotations

from dataclasses import dataclass
from functools import singledispatchmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils.interfaces import IParsable
from utils.utils import flatten, parse_value_between_strings


@dataclass(frozen=True)
class NumberRange:
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length - 1

    def intersection(self, number_range: NumberRange) -> Optional[NumberRange]:
        start = max(self.start, number_range.start)
        end = min(self.end, number_range.end)

        if start > end:
            return None

        return NumberRange(start=start, length=end - start + 1)

    def exceptwith(self, number_range: NumberRange) -> List[NumberRange]:
        intersection = self.intersection(number_range)
        if intersection == self:
            return []
        if intersection is None:
            return [self]
        if self.start == intersection.start:
            return [NumberRange(intersection.end + 1, self.end - intersection.end)]
        if self.end == intersection.end:
            return [NumberRange(self.start, intersection.start - self.start)]

        return [
            NumberRange(self.start, intersection.start - self.start),
            NumberRange(intersection.end + 1, self.end - intersection.end),
        ]


@dataclass(frozen=True)
class RangeMap(IParsable):
    source: NumberRange
    destination: NumberRange

    @singledispatchmethod
    def try_map(self, _: Any) -> Any:
        raise NotImplementedError

    @try_map.register(int)
    def _(self, num: int) -> Optional[int]:
        if self.source.start <= num < self.source.start + self.source.length:
            return self.destination.start + (num - self.source.start)

        return None

    @try_map.register(NumberRange)
    def _(self, number_range: NumberRange) -> Optional[NumberRange]:
        intersection = number_range.intersection(self.source)
        if intersection is None:
            return None
        return NumberRange(
            start=self.destination.start + (intersection.start - self.source.start),
            length=intersection.length,
        )

    @classmethod
    def parse(cls, string: str) -> "RangeMap":
        destination_start, source_start, range_length = string.split()
        return RangeMap(
            source=NumberRange(start=int(source_start), length=int(range_length)),
            destination=NumberRange(
                start=int(destination_start), length=int(range_length)
            ),
        )


@dataclass(frozen=True)
class Map(IParsable):
    source: str
    destination: str
    range_maps: List[RangeMap]

    @singledispatchmethod
    def map(self, _: Any) -> Any:
        raise NotImplementedError

    @map.register(int)
    def _(self, num: int) -> int:
        for range_map in self.range_maps:
            maybe_mapped_value = range_map.try_map(num)
            if maybe_mapped_value is not None:
                return maybe_mapped_value

        return num

    @map.register(NumberRange)
    def _(self, number_range: NumberRange) -> List[NumberRange]:
        mapped_ranges = []
        for range_map in self.range_maps:
            maybe_output_range = range_map.try_map(number_range)
            if maybe_output_range is not None:
                mapped_ranges.append(maybe_output_range)

        unmapped_ranges = [number_range]
        for range_map in self.range_maps:
            unmapped_ranges = flatten([
                number_range.exceptwith(range_map.source)
                for number_range in unmapped_ranges
            ])

        return mapped_ranges + unmapped_ranges

    @classmethod
    def parse(cls, string: str) -> "Map":
        lines = string.split("\n")
        return Map(
            source=parse_value_between_strings(lines[0], "", "-to-", str),
            destination=parse_value_between_strings(lines[0], "-to-", " map:", str),
            range_maps=[RangeMap.parse(line) for line in lines[1:]],
        )


def parse_seeds_as_ints(string: str) -> List[int]:
    return [int(n) for n in string[len("seeds: ") :].split()]


def parse_seeds_as_number_ranges(string: str) -> List[NumberRange]:
    seeds_as_ints = parse_seeds_as_ints(string)
    return [
        NumberRange(start, length)
        for start, length in zip(seeds_as_ints[::2], seeds_as_ints[1::2])
    ]


def traverse(seed: int, source_to_map: Dict[str, Map]) -> int:
    source = "seed"
    value = seed
    while source != "location":
        current_map = source_to_map[source]
        source = current_map.destination
        value = current_map.map(value)

    return value


def traverse_range(
    seed_range: NumberRange, source_to_map: Dict[str, Map]
) -> List[NumberRange]:
    source = "seed"
    number_ranges = [seed_range]
    while source != "location":
        current_map = source_to_map[source]
        source = current_map.destination
        number_ranges = flatten([
            current_map.map(input_range) for input_range in number_ranges
        ])

    return number_ranges


def main() -> None:
    sections = Path("input/input.txt").read_text("utf-8").split("\n\n")
    seeds = parse_seeds_as_ints(sections[0])
    maps = [Map.parse(section) for section in sections[1:]]
    source_to_map = {m.source: m for m in maps}

    lowest_location = min(traverse(seed, source_to_map) for seed in seeds)
    print(f"The lowest location number is {lowest_location}")

    seeds_as_ranges = parse_seeds_as_number_ranges(sections[0])
    location_ranges = flatten([
        traverse_range(seed_range, source_to_map) for seed_range in seeds_as_ranges
    ])
    print(
        "Interpreting the seeds as ranges, the lowest location number is"
        f" {min(r.start for r in location_ranges)}"
    )


if __name__ == "__main__":
    main()
