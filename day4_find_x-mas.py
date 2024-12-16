import re
from itertools import product
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


def detect_std_x(board: list[list[str]], row, col) -> bool:
    # checks for a X-MAS in the standard formation
    ret = board[row][col] == "A"
    ret &= board[row - 1][col - 1] == "M"
    ret &= board[row - 1][col + 1] == "S"
    ret &= board[row + 1][col - 1] == "M"
    ret &= board[row + 1][col + 1] == "S"
    # if ret:
    #     print(row, col, ret)

    return ret


def count_occurrences(input: list[list[str]]) -> int:
    rows = len(input)
    cols = len(input[0])
    count = 0
    for i, j in product(range(1, rows - 1), range(1, cols - 1)):
        count += detect_std_x(input, i, j)

    return count


def main() -> int:
    # global input
    input = get_input_lines_from_args()
    input = [list(line) for line in input]

    count = 0
    board = input.copy()

    # print_nice(board)
    count += count_occurrences(board)

    board = rotate(input)
    # print_nice(board)
    count += count_occurrences(board)

    board = invert_h(invert_v(input))
    # print_nice(board)
    count += count_occurrences(board)

    board = invert_h(invert_v(rotate(input)))
    # print_nice(board)
    count += count_occurrences(board)

    print("total", count)


if __name__ == "__main__":
    raise (SystemExit(main()))
