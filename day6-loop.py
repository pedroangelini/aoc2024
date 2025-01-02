from __future__ import annotations
from enum import Enum, auto, Flag, IntEnum
from utils.input_utils import get_input_from_args
from tqdm.auto import tqdm

# print = tqdm.write


class GameExitCode(Enum):
    GUARD_EXISTS = auto()
    GUARD_LOOPS = auto()


class GuardDirection(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class BoardTile(Flag):
    EMPTY = 0
    OBSTACLE = auto()
    GUARD_FACING_N = auto()
    GUARD_FACING_E = auto()
    GUARD_FACING_S = auto()
    GUARD_FACING_W = auto()
    STARTING = auto()
    WALKED_PATH_N = auto()
    WALKED_PATH_E = auto()
    WALKED_PATH_S = auto()
    WALKED_PATH_W = auto()


class Guard:
    position: tuple[int, int]
    direction: GuardDirection

    _move_map = {
        GuardDirection.N: (-1, 0),
        GuardDirection.E: (0, 1),
        GuardDirection.S: (1, 0),
        GuardDirection.W: (0, -1),
    }

    def __init__(
        self,
        position: tuple[int, int] | None = None,
        direction: GuardDirection | None = None,
    ):
        if position is None:
            position = (0, 0)
        if direction is None:
            direction = GuardDirection.N
        self.position = position
        self.direction = direction

    def naive_next_pos(self) -> tuple[int, int]:
        movement = self._move_map[self.direction]
        return (self.position[0] + movement[0], self.position[1] + movement[1])

    def next_direction(self) -> GuardDirection:
        if self.direction < 3:
            return GuardDirection(self.direction + 1)
        else:
            return GuardDirection.N

    def move_to(
        self, position: tuple[int, int], direction: GuardDirection | None = None
    ) -> None:
        self.position = position
        if direction is not None:
            self.direction = direction

    def __str__(self) -> str:
        return f"Guard at {self.position}, facing {repr(self.direction)}"


class BoardTickState(Enum):
    MOVE = auto()
    COLLIDE = auto()
    EXIT = auto()
    LOOP = auto()
    START = auto()


class Board:
    map: list[list[BoardTile]]
    guard: Guard
    shape: tuple[int, int]
    _str_tile_mapping = {
        "#": BoardTile.OBSTACLE,
        "^": BoardTile.GUARD_FACING_N,
        ">": BoardTile.GUARD_FACING_E,
        "v": BoardTile.GUARD_FACING_S,
        "<": BoardTile.GUARD_FACING_W,
        ".": BoardTile.EMPTY,
    }

    @classmethod
    def _map_tile_str(cls, tile: BoardTile) -> str:
        # _map_tile_str = {
        #     BoardTile.EMPTY: ".",
        #     BoardTile.OBSTACLE: "#",
        #     BoardTile.GUARD_FACING_N: "^",
        #     BoardTile.GUARD_FACING_E: ">",
        #     BoardTile.GUARD_FACING_S: "v",
        #     BoardTile.GUARD_FACING_W: "<",
        #     BoardTile.WALKED_PATH_N: "X",
        #     BoardTile.WALKED_PATH_E: "X",
        #     BoardTile.WALKED_PATH_S: "X",
        #     BoardTile.WALKED_PATH_W: "X",
        # }
        if not tile:
            return "."
        if tile & BoardTile.OBSTACLE:
            return "#"
        if tile & BoardTile.GUARD_FACING_N:
            return "^"
        if tile & BoardTile.GUARD_FACING_E:
            return ">"
        if tile & BoardTile.GUARD_FACING_S:
            return "v"
        if tile & BoardTile.GUARD_FACING_W:
            return "<"
        if tile & (
            BoardTile.WALKED_PATH_N
            | BoardTile.WALKED_PATH_E
            | BoardTile.WALKED_PATH_S
            | BoardTile.WALKED_PATH_W
        ):
            return "X"

    _map_tile_guard_orient = {
        BoardTile.GUARD_FACING_N: GuardDirection.N,
        BoardTile.GUARD_FACING_E: GuardDirection.E,
        BoardTile.GUARD_FACING_S: GuardDirection.S,
        BoardTile.GUARD_FACING_W: GuardDirection.W,
    }
    _map_walked_tile = {
        GuardDirection.N: BoardTile.WALKED_PATH_N,
        GuardDirection.E: BoardTile.WALKED_PATH_E,
        GuardDirection.S: BoardTile.WALKED_PATH_S,
        GuardDirection.W: BoardTile.WALKED_PATH_W,
    }
    _map_guard_orient_tile = {
        GuardDirection.N: BoardTile.GUARD_FACING_N,
        GuardDirection.E: BoardTile.GUARD_FACING_E,
        GuardDirection.S: BoardTile.GUARD_FACING_S,
        GuardDirection.W: BoardTile.GUARD_FACING_W,
    }

    def __init__(self, input: str | Board | None = None):
        if isinstance(input, str):
            self.map, self.guard = Board._board_from_str(input)
        elif isinstance(input, Board):
            self.map, self.guard = input._board_copy()
        elif input is None:
            self.map = list(list())
            self.guard = Guard((0, 0), GuardDirection.N)
        else:
            raise TypeError(f"Expected str or Board, got {type(input)}")

        if len(self.map) == 0:
            self.shape = (0, 0)
        else:
            self.shape = (len(self.map), len(self.map[0]))
            self.map[self.guard.position[0]][
                self.guard.position[1]
            ] |= BoardTile.STARTING

    @classmethod
    def _board_from_str(
        cls, str_input
    ) -> tuple[list[list[BoardTile]], list[int, int, GuardDirection]]:

        step1 = str_input.split("\n")
        step2 = [list(line) for line in step1]
        rows = len(step1)
        cols = len(step2[0])

        result: list[list[BoardTile]] = []
        for r in range(rows):
            line = []
            for c in range(cols):
                char = step2[r][c]
                try:
                    tile = cls._str_tile_mapping[char]
                except IndexError:
                    raise (
                        ValueError(
                            f"Invalid character in board: {c}. Can only process {'. '.join(list(cls._str_tile_mapping.keys()))}"
                        )
                    )
                line.append(tile)
                if tile & (
                    BoardTile.GUARD_FACING_N
                    | BoardTile.GUARD_FACING_E
                    | BoardTile.GUARD_FACING_S
                    | BoardTile.GUARD_FACING_S
                ):
                    guard = Guard((r, c), cls._map_tile_guard_orient[tile])

            result.append(line)

        return (result, guard)

    def _board_copy(self) -> Board:
        new_map = [line.copy() for line in self.map]
        new_guard = Guard(self.guard.position, self.guard.direction)
        return new_map, new_guard

    def tick(self):
        naive_next_pos = self.guard.naive_next_pos()

        # check if exiting the board
        if (
            naive_next_pos[0] < 0
            or naive_next_pos[0] >= self.shape[0]
            or naive_next_pos[1] < 0
            or naive_next_pos[1] >= self.shape[1]
        ):
            ret = BoardTickState.EXIT
            next_direction = self.guard.direction
            next_pos = naive_next_pos

        # check if colliding
        ## FIXME: colliding should just turn the guard and keep it in the same place
        elif self.map[naive_next_pos[0]][naive_next_pos[1]] & BoardTile.OBSTACLE:
            ret = BoardTickState.COLLIDE
            next_direction = self.guard.next_direction()
            # will not take care of case when the guard would have to turn twice
            next_pos = Guard(self.guard.position, next_direction).naive_next_pos()
        else:
            ret = BoardTickState.MOVE
            next_direction = self.guard.direction
            next_pos = naive_next_pos

        # update the current tile by removing the guard flag...
        self.map[self.guard.position[0]][
            self.guard.position[1]
        ] &= ~self._map_guard_orient_tile[self.guard.direction]
        # ... and adding the  walking flag of the current and next directions (in case the guard has turned)
        self.map[self.guard.position[0]][self.guard.position[1]] |= (
            self._map_walked_tile[self.guard.direction]
            | self._map_walked_tile[next_direction]
        )
        # then update the guard's
        self.guard.position = next_pos
        self.guard.direction = next_direction
        if ret != BoardTickState.EXIT:
            self.map[next_pos[0]][next_pos[1]] |= self._map_guard_orient_tile[
                next_direction
            ]

            # loop detection goes here - check if the guard has already moved in
            # same position, same direction

            if (
                self._map_walked_tile[self.guard.direction]
                & self.map[self.guard.position[0]][self.guard.position[1]]
            ):
                # print(f"loop detected in {self.guard.position}")
                ret = BoardTickState.LOOP
        print(repr(self))
        # update the map to add
        return ret

    def __str__(self):
        result = ""
        for r in range(self.shape[0]):
            line = ""
            for c in range(self.shape[1]):
                line = line + self._map_tile_str(self.map[r][c])
            result += line + "\n"
        return result

    def __repr__(self):
        return f"Board {str(self.shape)}\n{str(self)}\n{self.guard}"

    def count_walks(self) -> int:
        count = 0
        for r in range(self.shape[0]):
            for c in range(self.shape[1]):
                if self.map[r][c] & (
                    BoardTile.WALKED_PATH_N
                    | BoardTile.WALKED_PATH_E
                    | BoardTile.WALKED_PATH_S
                    | BoardTile.WALKED_PATH_W
                ):
                    count += 1
        return count


def run_game(input_board: Board) -> tuple[Board, BoardTickState]:
    board = Board(input_board)  # copy the input board to mutate
    ret = BoardTickState.START
    # progress_bar = tqdm()
    while ret not in (BoardTickState.EXIT, BoardTickState.LOOP):
        ret = board.tick()
        # progress_bar.update()

    return board, ret


def get_candidate_obstacles(complete_game: Board) -> list[tuple[int, int]]:

    candidates = []
    for r in range(complete_game.shape[0]):
        for c in range(complete_game.shape[1]):
            if (
                complete_game.map[r][c]
                & (
                    BoardTile.WALKED_PATH_N
                    | BoardTile.WALKED_PATH_E
                    | BoardTile.WALKED_PATH_S
                    | BoardTile.WALKED_PATH_W
                )
                & ~BoardTile.STARTING
                & ~BoardTile.OBSTACLE
            ):
                candidates.append((r, c))

    return candidates


def main() -> int:
    input_str = get_input_from_args()

    starting_board = Board(input_str)
    print("STARTING")
    print(repr(starting_board))
    baseline, exit_status = run_game(starting_board)
    print("---------")
    print("BASELINE")
    print(repr(baseline))
    print(f"exit status: {exit_status.name}")
    print(f"number of walks: {baseline.count_walks()}")
    exit()
    print("---------\n")
    print("getting possible obstacles")
    obstacle_candidates = get_candidate_obstacles(baseline)
    print(f"got {len(obstacle_candidates)}")

    print("---------\n")
    print("TESTING LOOPS")
    loop_count = 0
    for r, c in tqdm(obstacle_candidates):
        if starting_board.map[r][c] & (BoardTile.STARTING | BoardTile.OBSTACLE):
            continue

        test_board = Board(starting_board)
        test_board.map[r][c] = BoardTile.OBSTACLE
        _, exit_code = run_game(test_board)

        if exit_code == BoardTickState.LOOP:
            loop_count += 1
    print(f"\nloop count: {loop_count}")

    return 0


if __name__ == "__main__":
    # with Profile() as profile:
    exit(main())
    # Stats(profile).sort_stats(SortKey.TIME).print_stats()
