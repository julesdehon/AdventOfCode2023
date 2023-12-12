from dataclasses import dataclass
from math import prod
from pathlib import Path
from typing import List


@dataclass
class Race:
    time: int
    distance: int

    def winning_button_press_times(self) -> List[int]:
        winning_times = []
        for time_button_held in range(self.time + 1):
            speed = time_button_held
            distance = speed * (self.time - time_button_held)
            if distance > self.distance:
                winning_times.append(time_button_held)

        return winning_times


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8").split("\n")
    times = [int(t) for t in input_lines[0][len("Time:") :].split()]
    distances = [int(d) for d in input_lines[1][len("Distance:") :].split()]
    races = [Race(time=t, distance=d) for t, d in zip(times, distances)]
    winning_button_press_times = [race.winning_button_press_times() for race in races]
    print(
        "If you multiply the number of ways the record can be beaten for each race,"
        f" you get {prod(len(times) for times in winning_button_press_times)}"
    )

    single_race = Race(
        time=int("".join(str(t) for t in times)),
        distance=int("".join(str(d) for d in distances)),
    )
    print(len(single_race.winning_button_press_times()))


if __name__ == "__main__":
    main()
