
import re

from utils.input_utils import get_input_lines_from_args






def print_nice(board: list[list[str]]) -> None:

    for line in board:
        print(" ".join(line))

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
    global input
    input = get_input_lines_from_args()
    input = [list(line) for line in input]


if __name__ == "__main__":
#    raise (SystemExit(main()))
    main()
