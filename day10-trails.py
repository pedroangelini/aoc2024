from utils.input_utils import get_input_lines_from_args, str_seq_to_int_tup
from typing import Sequence


def print_nice(board: Sequence[Sequence[int]]) -> None:
    for line in board:
        print(" ".join((str(pos) for pos in line)))

    print("-" * 20)


def traverse_trail(
    board: Sequence[Sequence[int]], starting_pos: tuple[int, int]
) -> set[tuple[int, int]]:

    visited: set[tuple[int, int]] = set()
    visit_queue: list[tuple[int, int]] = [starting_pos]
    trail_ends = set()

    while visit_queue:
        # print(f"{visit_queue=}")
        # print(f"{visited=}")
        # print(f"{trail_ends=}")
        current = visit_queue.pop()
        # print(f"{current=}")

        visited.add(current)

        # found a trail end
        if board[current[0]][current[1]] == 9:
            trail_ends.add(current)
            continue

        # no trail end, let's check the neighbors
        # check up
        if (
            current[0] > 0
            and board[current[0] - 1][current[1]] == board[current[0]][current[1]] + 1
            and board[current[0] - 1][current[1]] not in visited
        ):
            visit_queue.append((current[0] - 1, current[1]))
        # check down
        if (
            current[0] < len(board) - 1
            and board[current[0] + 1][current[1]] == board[current[0]][current[1]] + 1
            and board[current[0] + 1][current[1]] not in visited
        ):
            visit_queue.append((current[0] + 1, current[1]))
        # check right
        if (
            current[1] < len(board[0]) - 1
            and board[current[0]][current[1] + 1] == board[current[0]][current[1]] + 1
            and board[current[0]][current[1] + 1] not in visited
        ):
            visit_queue.append((current[0], current[1] + 1))
        # check left
        if (
            current[1] > 0
            and board[current[0]][current[1] - 1] == board[current[0]][current[1]] + 1
            and board[current[0]][current[1] - 1] not in visited
        ):
            visit_queue.append((current[0], current[1] - 1))

    return trail_ends


def main() -> int:
    board = get_input_lines_from_args()
    board: tuple[tuple] = tuple(str_seq_to_int_tup(l) for l in board)

    print_nice(board)

    total = 0
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == 0:
                trail_ends = traverse_trail(board, (r, c))
                print(f"f{(r, c)} -- {len(trail_ends)} -- {trail_ends}")
                total += len(trail_ends)

    print(f"{total = }")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
