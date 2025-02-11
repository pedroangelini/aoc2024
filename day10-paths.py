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


def recursive_traverse(
    board: Sequence[Sequence[int]], traversed: tuple[tuple[int, int]]
) -> tuple[tuple[int, int]]:

    # base case
    current_pos = traversed[-1]
    print(f"{traversed = }")
    print(f"{current_pos = }")
    if board[current_pos[0]][current_pos[1]] == 9:
        print("found end of trail")
        return traversed

    next_steps = find_next_steps(board, current_pos)
    print(f"{next_steps = }")

    # for next_step in next_steps:
    for next_step in next_steps:
        print(f"processing {next_step = }")
        new_traversed = traversed + (next_step,)
        return recursive_traverse(board, new_traversed)


def main() -> int:
    board = get_input_lines_from_args()
    board: tuple[tuple] = tuple(str_seq_to_int_tup(l) for l in board)

    print_nice(board)

    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == 0:
                trail = recursive_traverse(board, ((r, c),))

    print(f"{trail = }")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
