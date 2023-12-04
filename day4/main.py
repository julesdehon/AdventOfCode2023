from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

from utils.interfaces import IParsable
from utils.utils import parse_value_between_strings


@dataclass
class Card(IParsable):
    card_id: int
    _winning_numbers: Set[int]
    _your_numbers: Set[int]

    @classmethod
    def parse(cls, string: str) -> "Card":
        card_id = parse_value_between_strings(
            string, "Card", ":", lambda v: int(v.strip())
        )
        string = string[string.find(":") + 1 :]
        raw_winning_numbers, raw_your_numbers = string.split(" | ")
        winning_numbers = {int(num) for num in raw_winning_numbers.split()}
        your_numbers = {int(num) for num in raw_your_numbers.split()}

        return Card(
            card_id=card_id,
            _winning_numbers=winning_numbers,
            _your_numbers=your_numbers,
        )

    @property
    def your_winning_numbers(self) -> Set[int]:
        return self._winning_numbers.intersection(self._your_numbers)

    def get_points(self) -> int:
        if len(self.your_winning_numbers) == 0:
            return 0
        return 2 ** (len(self.your_winning_numbers) - 1)


def process_cards(cards: List[Card]) -> Dict[int, int]:
    card_id_to_num_copies = {card.card_id: 1 for card in cards}
    for card in sorted(cards, key=lambda card: card.card_id):
        num_copies = card_id_to_num_copies[card.card_id]
        num_winning_numbers = len(card.your_winning_numbers)
        for card_id in range(card.card_id + 1, card.card_id + num_winning_numbers + 1):
            card_id_to_num_copies[card_id] += num_copies

    return card_id_to_num_copies


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8").split("\n")
    cards = [Card.parse(line) for line in input_lines if line != ""]
    print(
        "In total, the scratch cards are worth"
        f" {sum(card.get_points() for card in cards)}"
    )
    card_id_to_num_copies = process_cards(cards)
    print(
        "After processing all cards, you end up with"
        f" {sum(num_copies for num_copies in card_id_to_num_copies.values())} total"
        " scratch cards"
    )


if __name__ == "__main__":
    main()
