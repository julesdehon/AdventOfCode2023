from pathlib import Path
from typing import Callable, List

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


def calibration_value_from_digits(line: str) -> int:
    numbers = [int(char) for char in line if char.isdigit()]
    return numbers[0] * 10 + numbers[-1]


def calibration_value_from_digits_or_spelled(line: str) -> int:
    numbers = []
    for i, char in enumerate(line):
        if char.isdigit():
            numbers.append(int(char))
        for word, digit in WORD_TO_NUMBER.items():
            if line[i:].startswith(word):
                numbers.append(digit)

    return numbers[0] * 10 + numbers[-1]


def calibration_sum(
    calibration_document: List[str], get_calibration_value: Callable[[str], int]
) -> int:
    return sum(get_calibration_value(line) for line in calibration_document)


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8").split("\n")

    sum_of_calibration_values_using_digits = calibration_sum(
        input_lines, calibration_value_from_digits
    )
    print(
        "The sum of all the calibration values using only digits was"
        f" {sum_of_calibration_values_using_digits}"
    )

    sum_of_calibration_values_using_digits_and_words = calibration_sum(
        input_lines, calibration_value_from_digits_or_spelled
    )
    print(
        "The sum of all the calibration values using digits and words was"
        f" {sum_of_calibration_values_using_digits_and_words}"
    )


if __name__ == "__main__":
    main()
