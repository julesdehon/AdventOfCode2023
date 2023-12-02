from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from utils.interfaces import IParsable
from utils.utils import parse_value_between_strings


@dataclass(frozen=True)
class Handful(IParsable):
    blue: int
    red: int
    green: int

    @classmethod
    def parse(cls, string: str) -> "Handful":
        raw_subsets = string.split(", ")
        colour_to_count: Dict[str, int] = defaultdict(int)
        for raw_subset in raw_subsets:
            count, colour = raw_subset.split(" ")
            colour_to_count[colour] += int(count)
        return Handful(
            blue=colour_to_count["blue"],
            red=colour_to_count["red"],
            green=colour_to_count["green"],
        )

    def power(self) -> int:
        return self.blue * self.red * self.green


@dataclass(frozen=True)
class Game(IParsable):
    game_id: int
    handfuls: List[Handful]

    @classmethod
    def parse(cls, string: str) -> "Game":
        game_id = parse_value_between_strings(
            string, before="Game ", after=":", parse=int
        )
        raw_handfuls = string[len(f"Game {game_id}: ") :]
        return Game(
            game_id,
            [Handful.parse(raw_handful) for raw_handful in raw_handfuls.split("; ")],
        )

    def minimum_set_for_game_to_be_possible(self) -> Handful:
        return Handful(
            blue=max(handful.blue for handful in self.handfuls),
            red=max(handful.red for handful in self.handfuls),
            green=max(handful.green for handful in self.handfuls),
        )


@dataclass(frozen=True)
class Constraint:
    max_blue: int
    max_red: int
    max_green: int

    def breached(self, handful: Handful) -> bool:
        return (
            handful.blue > self.max_blue
            or handful.red > self.max_red
            or handful.green > self.max_green
        )


def main() -> None:
    games = [
        Game.parse(line)
        for line in Path("input/input.txt").read_text("utf-8").split("\n")
    ]
    constraint = Constraint(max_blue=14, max_red=12, max_green=13)
    possible_games = [
        game
        for game in games
        if not any(constraint.breached(handful) for handful in game.handfuls)
    ]
    print(
        f"The sum of the possible game IDs is {sum(game.game_id for game in possible_games)}"
    )

    minimum_sets = [game.minimum_set_for_game_to_be_possible() for game in games]
    print(
        "The sum of the power of all the minimum sets is "
        f"{sum(minimum_set.power() for minimum_set in minimum_sets)}"
    )


if __name__ == "__main__":
    main()
