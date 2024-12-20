from __future__ import annotations
from utils.input_utils import get_input_from_args
from copy import deepcopy
import itertools


def next_orientation():
    _cycle = itertools.cycle("^>v<")
    yield _cycle.__next__()


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


def main() -> int:
    input = get_input_from_args()
    board = Board(input)
    print(repr(board))
    print("-----------------")

    print(orientation := next_orientation())
    print(orientation := next_orientation())
    print(orientation := next_orientation())
    print(orientation := next_orientation())


if __name__ == "__main__":
    raise SystemExit(main())
