from utils.input_utils import get_input_lines_from_args
import itertools


def print_nice(board: list[list[str]], title: str | None = None) -> None:

    if title is not None:
        print(title)

    for line in board:
        print(" ".join(line))

    print("-" * 30)


def find_antennas(board: list[list[str]]) -> None:
    heigh = len(board)
    width = len(board[0])

    antennas: dict[list[tuple]] = dict()

    for r in range(heigh):
        for c in range(width):

            char = board[r][c]

            if char in (".", "#"):
                continue

            if char in antennas:
                antennas[char].append((r, c))
            else:
                antennas[char] = [
                    (r, c),
                ]

    return antennas


def find_antinodes(
    antenna1: tuple[int, int], antenna2: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    anti1 = (
        antenna2[0] + (antenna2[0] - antenna1[0]),
        antenna2[1] + (antenna2[1] - antenna1[1]),
    )
    anti2 = (
        antenna1[0] + (antenna1[0] - antenna2[0]),
        antenna1[1] + (antenna1[1] - antenna2[1]),
    )
    return anti1, anti2


def count_antinodes(antinode_board: list[list[str]]) -> int:
    heigh = len(antinode_board)
    width = len(antinode_board[0])

    antinode_count: int = 0

    for r in range(heigh):
        for c in range(width):
            if antinode_board[r][c] == "#":
                antinode_count += 1

    return antinode_count


def main() -> int:
    input_str = get_input_lines_from_args()
    antenna_map = [list(line) for line in input_str]
    heigh = len(antenna_map)
    width = len(antenna_map[0])

    antinode_map = [list("." * width) for _ in range(heigh)]
    print_nice(antenna_map, "antenna_map")
    # print_nice(antinode_map, "antinode_map")

    all_antennas = find_antennas(antenna_map)
    # print(all_antennas)

    for antenna_list in all_antennas.values():
        pairs = itertools.combinations(antenna_list, r=2)
        for pair in pairs:
            a1, a2 = find_antinodes(pair[0], pair[1])
            if (0 <= a1[0] < heigh) and (0 <= a1[1] < heigh):
                antinode_map[a1[0]][a1[1]] = "#"

            if (0 <= a2[0] < heigh) and (0 <= a2[1] < heigh):
                antinode_map[a2[0]][a2[1]] = "#"

            # print_nice(antinode_map, title=f"antinode map with pair {pair}")

    print_nice(antinode_map, "antinode_map")
    print(f"total antinodes: {count_antinodes(antinode_map)}")


if __name__ == "__main__":
    raise (SystemExit(main()))
