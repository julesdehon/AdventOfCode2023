from dataclasses import dataclass
from enum import Enum
from itertools import cycle
from math import lcm
from pathlib import Path
from typing import Dict

from utils.interfaces import IParsable

START_NODE = "AAA"
END_NODE = "ZZZ"


class Instruction(Enum):
    RIGHT = "R"
    LEFT = "L"


@dataclass(frozen=True)
class Node(IParsable):
    name: str
    left: str
    right: str

    def get(self, instruction: Instruction) -> str:
        if instruction == Instruction.LEFT:
            return self.left
        if instruction == Instruction.RIGHT:
            return self.right

        raise Exception(f"Unknown instruction: {instruction}")

    @classmethod
    def parse(cls, string: str) -> "Node":
        name, rest = string.split(" = ")
        left, right = rest[1:-1].split(", ")
        return Node(name=name, left=left, right=right)


@dataclass(frozen=True)
class Map(IParsable):
    value_to_node: Dict[str, Node]

    def get(self, node_name: str) -> Node:
        assert node_name in self.value_to_node, f"No node found with name {node_name}"
        return self.value_to_node[node_name]

    @classmethod
    def parse(cls, string: str) -> "Map":
        nodes = [Node.parse(n) for n in string.splitlines()]
        return Map({node.name: node for node in nodes})


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8")
    raw_instructions, raw_map = input_lines.split("\n\n")
    instructions = cycle([Instruction(i) for i in raw_instructions])
    node_map = Map.parse(raw_map)

    current_node = START_NODE
    steps = 0
    while current_node != END_NODE:
        instruction = next(instructions)
        current_node = node_map.get(current_node).get(instruction)
        steps += 1

    print(f"It took {steps} steps to get to {END_NODE}")

    starting_nodes = [
        node for node in node_map.value_to_node.keys() if node.endswith("A")
    ]
    cycle_lengths = {}
    for node in starting_nodes:
        next_node = node
        instructions = cycle([Instruction(i) for i in raw_instructions])
        for step, instruction in enumerate(instructions):
            if next_node.endswith("Z"):
                cycle_lengths[node] = step
                break
            next_node = node_map.get(next_node).get(instruction)

    print(
        f"It took {lcm(*cycle_lengths.values())} before I was only on nodes that end"
        " in Z"
    )


if __name__ == "__main__":
    main()
