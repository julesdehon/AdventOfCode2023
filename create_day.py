import subprocess
import sys
from pathlib import Path

YEAR = 2023
PROJECT_ROOT = Path(__file__).parent.resolve()
TEMPLATE = r"""from pathlib import Path


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8").split("\n")


if __name__ == "__main__":
    main()
"""


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python create_day.py <day number>")
        return

    day = int(sys.argv[1])

    day_directory = PROJECT_ROOT / f"day{day}"
    try:
        day_directory.mkdir()
    except FileExistsError:
        print(f"Could not create {day_directory} since it already existed")
        return

    (day_directory / "__init__.py").write_text("")
    (day_directory / "main.py").write_text(TEMPLATE)
    input_directory = day_directory / "input"
    input_directory.mkdir()

    # See https://github.com/GreenLightning/advent-of-code-downloader to set up input downloader
    try:
        subprocess.run(
            [
                f"{PROJECT_ROOT / 'toolchain' / 'aocdl'}",
                "-year",
                str(YEAR),
                "-day",
                str(day),
                "-output",
                str((input_directory / "input.txt").resolve()),
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        print(f"Could not download input for {YEAR=} {day=}")


if __name__ == "__main__":
    main()
