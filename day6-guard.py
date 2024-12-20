
from __future__ import annotations
from utils.input_utils import get_input_from_args
from copy import deepcopy
from enum import Enum, auto


guard_cycle = {
    "^":(-1, 0),
    ">":( 0, 1),
    "v":( 1, 0),
    "<":( 0, 1),
}


def orientation_gen():
    global guard_cycle

    cur_pos =-1
    while True:
        cur_pos += 1
        if cur_pos == len(guard_cycle):
            cur_pos = 0
        yield list(guard_cycle.keys())[cur_pos]

orientation_cycle= orientation_gen()

class BoardState(Enum):
    WALKING = auto()
    BLOCKED = auto()
    EXITED = auto()

class Board:
    _map: list[list[str]]

    def __init__(self, input: str):
        tmp = input.split("\n")
        self._map = [list(line) for line in tmp]

    @classmethod
    def from_board(cls, input_board: Board) -> Board:
        b = Board("")
        b._map = deepcopy(input_board._map)
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
                f"Value needs to be a 1 character string, but got {value}, lenght {len(value)}"
            )
        b = Board.from_board(self)

        b._map[line][col] = value
        return b

    def char_count(self, char: str) -> int:
        s = str(self)

    def find_char(self, char) -> tuple[int, int]|None:
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

    @property
    def state(self) -> BoardState:
        ...


def next_frame(board: Board) -> Boars:
    #match boaed.state:
    return None



def main() -> int:
    input = get_input_from_args()
    board = Board(input)
    print(repr(board))
    print("-----------------")

    #print(next(orientation_cycle))
    guard_orient = next(orientation_cycle)
    print(board.find_guard())


if __name__ == "__main__":
    raise SystemExit(main())
