from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from pathlib import Path
from typing import List

CARDS_ORDER = "AKQJT98765432"
JOKER_ENABLED_CARDS_ORDER = "AKQT98765432J"


@total_ordering
class Type(Enum):
    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_A_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6

    def __lt__(self, other: "Type") -> bool:
        return other.value < self.value


@total_ordering
@dataclass(frozen=True)
class Card:
    card: str
    joker_enabled: bool

    @classmethod
    def parse(cls, string: str, joker_enabled: bool = False) -> "Card":
        assert len(string) == 1, f"Expected {string} to have length 1"
        assert string in CARDS_ORDER, f"Expected {string} to be on of {CARDS_ORDER}"

        return Card(string, joker_enabled)

    def __lt__(self, other: "Card") -> bool:
        card_order = JOKER_ENABLED_CARDS_ORDER if self.joker_enabled else CARDS_ORDER
        return card_order.index(other.card) < card_order.index(self.card)


@total_ordering
@dataclass(frozen=True)
class Hand:
    JOKER = Card.parse("J", joker_enabled=True)
    ACE = Card.parse("A")

    cards: List[Card]

    @classmethod
    def parse(cls, string: str, joker_enabled: bool = False) -> "Hand":
        return Hand([Card.parse(c, joker_enabled) for c in string])

    @property
    def _type_without_jokers(self) -> Type:
        assert (
            self.JOKER not in self.cards
        ), "Called _type_without_jokers on a Hand that had jokers"

        occurrences = Counter(self.cards).values()
        if 5 in occurrences:
            return Type.FIVE_OF_A_KIND
        if 4 in occurrences:
            return Type.FOUR_OF_A_KIND
        if 3 in occurrences and 2 in occurrences:
            return Type.FULL_HOUSE
        if 3 in occurrences:
            return Type.THREE_OF_A_KIND
        if len([o for o in occurrences if o == 2]) == 2:
            return Type.TWO_PAIR
        if 2 in occurrences:
            return Type.ONE_PAIR

        return Type.HIGH_CARD

    @property
    def type(self) -> Type:
        if self.JOKER not in self.cards:
            return self._type_without_jokers

        cards_to_occurrences = Counter(self.cards)
        most_common_card, _ = max(
            [(c, o) for c, o in cards_to_occurrences.items() if c != self.JOKER],
            key=lambda x: x[1],
            default=(self.ACE, 0),
        )

        return Hand(
            ([most_common_card] * cards_to_occurrences[self.JOKER])
            + [c for c in self.cards if c != self.JOKER]
        ).type

    def __lt__(self, other: "Hand") -> bool:
        if self.type != other.type:
            return self.type < other.type

        for self_card, other_card in zip(self.cards, other.cards):
            if self_card != other_card:
                return self_card < other_card

        return False


@total_ordering
@dataclass(frozen=True)
class Turn:
    hand: Hand
    bid: int

    @classmethod
    def parse(cls, string: str, joker_enabled: bool = False) -> "Turn":
        h, b = string.split()
        return Turn(Hand.parse(h, joker_enabled), int(b))

    def __lt__(self, other: "Turn") -> bool:
        return self.hand < other.hand


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8").split("\n")
    turns = [Turn.parse(t) for t in input_lines if t != ""]
    sorted_turns = sorted(turns)
    print(
        "Total winnings:"
        f" {sum(turn.bid * (rank + 1) for rank, turn in enumerate(sorted_turns))}"
    )

    joker_enabled_turns = [
        Turn.parse(t, joker_enabled=True) for t in input_lines if t != ""
    ]
    sorted_joker_enabled_turns = sorted(joker_enabled_turns)
    print(
        "Total winnings:"
        f" {sum(turn.bid * (rank + 1) for rank, turn in enumerate(sorted_joker_enabled_turns))}"
    )


if __name__ == "__main__":
    main()
