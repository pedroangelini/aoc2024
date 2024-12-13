from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme
import rich
import re

from utils.input_utils import get_input_lines_from_args


class XMASHighlighter(RegexHighlighter):
    """Apply style to XMAS"""

    base_style = "example."
    highlights = [r"(?P<XMAS>X M A S)"]


xmas_theme = Theme({"example.XMAS": "bold red"})
console = Console(highlighter=XMASHighlighter(), theme=xmas_theme)


def print_nice(board: list[list[str]]) -> None:

    for line in board:
        console.print(" ".join(line))

    print("-" * 20)


def s2l(s: str) -> list[str]:
    return [c for c in s]


def empty_board(rows: int, cols: int | None = None) -> list[list[str]]:
    if cols is None:
        cols = rows
    return [list("_" * cols) for _ in range(rows)]


def rotate(board: list[list[str]]) -> list[list[str]]:
    rotated = empty_board(len(board[0]))
    # print_nice(rotated)
    for i in range(len(board)):  # lines
        for j in range(len(board[0])):  # cols
            rotated[j][i] = board[i][j]

    return rotated


def invert_h(board: list[list[str]]) -> list[list[str]]:
    cols = len(board[0])
    inverted = empty_board(len(board))
    # print_nice(rotated)
    for i in range(len(board)):  # lines
        for j in range(cols):  # cols
            inverted[i][j] = board[i][cols - j - 1]

    return inverted


def invert_v(board: list[list[str]]) -> list[list[str]]:
    rows = len(board)
    cols = len(board[0])
    inverted = empty_board(rows)
    # print_nice(rotated)
    for i in range(rows):  # lines
        for j in range(cols):  # cols

            inverted[i][j] = board[rows - i - 1][j]

    return inverted


def skew_up(board: list[list[str]]) -> list[list[str]]:
    rows = len(board)
    cols = len(board[0])
    skewed = empty_board(rows * 2 - 1, cols)
    # print_nice(rotated)
    for i in range(rows):  # lines
        for j in range(cols):  # cols
            skewed[i + rows - 1 - j][j] = board[i][j]

    return skewed


def skew_down(board: list[list[str]]) -> list[list[str]]:
    rows = len(board)
    cols = len(board[0])
    skewed = empty_board(rows * 2 - 1, cols)
    # print_nice(rotated)
    for i in range(rows):  # lines
        for j in range(cols):  # cols
            skewed[i + j][j] = board[i][j]

    return skewed


def count_occurrences(input: list[list[str]]) -> int:
    all_str = "\n".join("".join(l) for l in input)
    matcher = re.compile(r"XMAS")
    return len(matcher.findall(all_str))


def main() -> int:
    input = get_input_lines_from_args()
    input = [list(line) for line in input]

    right_count = count_occurrences(input)
    print(f"right {right_count}")
    print_nice(input)

    down_right = skew_up(input)
    down_right_count = count_occurrences(down_right)
    print(f"bottom-right {down_right_count}")
    print_nice(down_right)

    down = rotate(input)
    down_count = count_occurrences(down)
    print(f"down {down_count}")
    print_nice(down)

    down_left = skew_down(rotate(input))
    down_left_count = count_occurrences(down_left)
    print(f"down-left {down_left_count}")
    print_nice(down_left)

    left = invert_h(input)
    left_count = count_occurrences(left)
    print(f"left {left_count}")
    print_nice(left)

    up_left = skew_down(invert_h(input))
    up_left_count = count_occurrences(up_left)
    print(f"up-left {up_left_count}")
    print_nice(up_left)

    up = rotate(invert_v(input))
    up_count = count_occurrences(up)
    print(f"up {up_count}")
    print_nice(up)

    up_right = skew_down(input)
    up_right_count = count_occurrences(up_right)
    print(f"up-right {up_right_count}")
    print_nice(up_right)

    print()
    print(
        f"total = {right_count + down_right_count + down_count + down_left_count + left_count + up_left_count + up_count + up_right_count}"
    )


if __name__ == "__main__":
    raise (SystemExit(main()))
