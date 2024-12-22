from __future__ import annotations
from utils.input_utils import get_input_from_args
from copy import deepcopy
from enum import Enum, auto
from cProfile import Profile
from pstats import SortKey, Stats

# from time import sleep
from tqdm import tqdm


guard_cycle = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def orientation_gen():
    global guard_cycle

    cur_pos = -1
    while True:
        cur_pos += 1
        if cur_pos == len(guard_cycle):
            cur_pos = 0
        yield list(guard_cycle.keys())[cur_pos]


orientation_cycle = orientation_gen()


class BoardNextState(Enum):
    MOVE = auto()
    COLLIDE = auto()
    EXIT = auto()


class Board:
    _map: list[list[str]]

    def __init__(self, input: str):
        tmp = input.split("\n")
        self._map = [list(line) for line in tmp]

    @classmethod
    def from_board(cls, input_board: Board) -> Board:
        b = Board(str(input_board))
        # b._map = deepcopy(input_board._map)
        return b

    def __str__(self):
        return "\n".join(["".join(line) for line in self._map])

    def __repr__(self):
        return f"Board {str(self.shape)}\n{str(self)}"

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self._map), len(self._map[0]))

    def with_value(self, value: str, line: int, col: int) -> Board:
        value = str(value)
        if len(value) != 1:
            raise ValueError(
                f"Value needs to be a 1 character string, but got {value}, length {len(value)}"
            )
        b = Board.from_board(self)

        b._map[line][col] = value
        return b

    def char_count(self, char: str) -> int:
        s = str(self)
        return s.count(char)

    def find_char(self, char) -> tuple[int, int] | None:
        lines, cols = self.shape
        for l in range(lines):
            for c in range(cols):
                if self._map[l][c] == char:
                    return (l, c)
        return None

    def find_guard(self) -> tuple[int, int, str]:
        for g in guard_cycle:
            found = self.find_char(g)
            if found is not None:
                return (*found, g)

    def next_move(self) -> tuple[int, int]:
        g_row, g_col, facing = self.find_guard()
        go_to = guard_cycle[facing]
        return (g_row + go_to[0], g_col + go_to[1])

    @property
    def next_state(self) -> BoardNextState:
        next_location = self.next_move()
        if (
            next_location[0] < 0
            or next_location[1] < 0
            or next_location[0] >= self.shape[0]
            or next_location[1] >= self.shape[1]
        ):
            return BoardNextState.EXIT
        if self._map[next_location[0]][next_location[1]] == "#":
            return BoardNextState.COLLIDE
        return BoardNextState.MOVE


def next_board(board: Board) -> tuple[Board, bool]:
    cur_row, cur_col, guard = board.find_guard()
    next_state = board.next_state
    next_row, next_col = board.next_move()
    # print(next_state.name)
    match next_state:
        case BoardNextState.EXIT:
            return (board.with_value("X", cur_row, cur_col), True)
        case BoardNextState.MOVE:
            return (
                board.with_value("X", cur_row, cur_col).with_value(
                    guard, next_row, next_col
                ),
                False,
            )
        case BoardNextState.COLLIDE:
            next_guard = next(orientation_cycle)
            # print(next_guard)
            temp_board = board.with_value(next_guard, cur_row, cur_col)
            next_row, next_col = temp_board.next_move()
            return (
                temp_board.with_value("X", cur_row, cur_col).with_value(
                    next_guard, next_row, next_col
                ),
                False,
            )


def main() -> int:
    input_str = get_input_from_args()

    # find initial orientation and set the iterator
    while True:
        orient = next(orientation_cycle)
        if orient in input_str:
            break
    print(f"starting orientation: {orient}")

    board = Board(input_str)
    # print(chr(27) + "[2J")
    print(board)
    print("-----------------")
    # sleep(0.1)
    # input()

    pbar = tqdm()
    f = 0
    while True:
        board, done = next_board(board)

        # print(chr(27) + "[2J")
        f += 1
        if f == 1000:
            print()
            print(board)
            print(f"----------------- {board.char_count("X")} Xs")
            f = 0

        # sleep(0.1)
        # input()
        pbar.update()
        if done:
            break

    print()
    print(board)
    print("-----------------")
    print(f"walked {board.char_count("X")} positions")


if __name__ == "__main__":
    # with Profile() as profile:
    main()
    # Stats(profile).sort_stats(SortKey.TIME).print_stats()
