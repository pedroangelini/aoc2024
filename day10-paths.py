from utils.input_utils import get_input_lines_from_args, str_seq_to_int_tup
from typing import Sequence


def print_nice(board: Sequence[Sequence[int]]) -> None:
    for line in board:
        print(" ".join((str(pos) for pos in line)))

    print("-" * 20)


def find_next_steps(
    board: Sequence[Sequence[int]], current: tuple[int, int]
) -> list[tuple[int, int]]:
    next_steps = list()
    # check up
    if (
        current[0] > 0
        and board[current[0] - 1][current[1]] == board[current[0]][current[1]] + 1
    ):
        next_steps.append((current[0] - 1, current[1]))
    # check down
    if (
        current[0] < len(board) - 1
        and board[current[0] + 1][current[1]] == board[current[0]][current[1]] + 1
    ):
        next_steps.append((current[0] + 1, current[1]))
    # check right
    if (
        current[1] < len(board[0]) - 1
        and board[current[0]][current[1] + 1] == board[current[0]][current[1]] + 1
    ):
        next_steps.append((current[0], current[1] + 1))
    # check left
    if (
        current[1] > 0
        and board[current[0]][current[1] - 1] == board[current[0]][current[1]] + 1
    ):
        next_steps.append((current[0], current[1] - 1))

    return next_steps


def find_rating(board: Sequence[Sequence[int]], starting: tuple[int, int]) -> int:

    next_steps = [starting]
    found_ends = 0

    while next_steps:
        current = next_steps.pop()
        print(f"{current=}")

        if board[current[0]][current[1]] == 9:
            found_ends = found_ends + 1
            continue

        next_steps += find_next_steps(board, current)
        print(f"{next_steps=}")

    return found_ends


def main() -> int:
    board = get_input_lines_from_args()
    board: tuple[tuple] = tuple(str_seq_to_int_tup(l) for l in board)

    print_nice(board)
    total_ratings = 0

    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == 0:
                total_ratings += find_rating(board, (r, c))

    print(f"{total_ratings = }")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
