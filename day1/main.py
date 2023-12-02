from dataclasses import dataclass
from pathlib import Path
from typing import List, Callable

from utils.utils import flatten

WORD_TO_NUMBER = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


@dataclass
class NumberAndPosition:
    number: int
    position: int


def find_all(substring: str, string: str) -> List[int]:
    return [i for i in range(len(string)) if string.startswith(substring, i)]


def calibration_value_from_digits(line: str) -> int:
    numbers = [int(char) for char in line if char.isdigit()]
    return numbers[0] * 10 + numbers[-1]


def calibration_value_from_digits_or_spelled(line: str) -> int:
    word_number_and_positions = flatten(
        [
            [
                NumberAndPosition(WORD_TO_NUMBER[word], index)
                for index in find_all(word, line)
            ]
            for word in WORD_TO_NUMBER
            if word in line
        ]
    )
    numeric_number_and_positions = [
        NumberAndPosition(int(char), index)
        for index, char in enumerate(line)
        if char.isdigit()
    ]
    sorted_numbers = [
        np.number
        for np in sorted(
            word_number_and_positions + numeric_number_and_positions,
            key=lambda np: np.position,
        )
    ]

    return sorted_numbers[0] * 10 + sorted_numbers[-1]


def calibration_sum(
    calibration_document: List[str], get_calibration_value: Callable[[str], int]
) -> int:
    return sum(get_calibration_value(line) for line in calibration_document)


def main() -> None:
    input_lines = Path("input/input.txt").read_text().split("\n")

    sum_of_calibration_values_using_digits = calibration_sum(
        input_lines, calibration_value_from_digits
    )
    print(
        f"The sum of all the calibration values using only digits was {sum_of_calibration_values_using_digits}"
    )

    sum_of_calibration_values_using_digits_and_words = calibration_sum(
        input_lines, calibration_value_from_digits_or_spelled
    )
    print(
        f"The sum of all the calibration values using digits and words was {sum_of_calibration_values_using_digits_and_words}"
    )


if __name__ == "__main__":
    main()
