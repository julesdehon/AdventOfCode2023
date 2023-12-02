from typing import Callable, List, Optional, TypeVar

T = TypeVar("T")


def flatten(list_of_lists: List[List[T]]) -> List[T]:
    return [item for sublist in list_of_lists for item in sublist]


def try_parse_value_between_strings(
    string: str, before: str, after: str, parse: Callable[[str], T]
) -> Optional[T]:
    before_idx = string.find(before)
    if before_idx == -1:
        return None
    before_idx += len(before)

    after_idx = string[before_idx:].find(after)
    if after_idx == -1:
        return None

    return parse(string[before_idx : before_idx + after_idx])


def parse_value_between_strings(
    string: str, before: str, after: str, parse: Callable[[str], T]
) -> T:
    maybe_value_between_strings = try_parse_value_between_strings(
        string, before, after, parse
    )
    assert (
        maybe_value_between_strings is not None
    ), f"Could not find {before} or {after} in {string}"

    return maybe_value_between_strings
