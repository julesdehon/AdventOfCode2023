from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List

from utils.interfaces import IParsable


class Direction(Enum):
    Forward = (-1, 1)
    Backward = (0, -1)


@dataclass(frozen=True)
class Sequence(IParsable):
    sequence: List[int]

    @classmethod
    def parse(cls, string: str) -> "Sequence":
        return Sequence([int(v) for v in string.split()])

    def extrapolate(self, direction: Direction) -> int:
        if all(n == 0 for n in self.sequence):
            return 0

        start_idx, multiplier = direction.value

        return self.sequence[start_idx] + multiplier * Sequence([
            a - b for a, b in zip(self.sequence[1:], self.sequence[:-1])
        ]).extrapolate(direction)


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8").split("\n")
    sequences = [Sequence.parse(line) for line in input_lines]
    print(
        "Extrapolating forwards, the sum of extrapolated values is"
        f" {sum(sequence.extrapolate(Direction.Forward) for sequence in sequences)}"
    )
    print(
        "Extrapolating backwards, the sum of extrapolated values is"
        f" {sum(sequence.extrapolate(Direction.Backward) for sequence in sequences)}"
    )


if __name__ == "__main__":
    main()
