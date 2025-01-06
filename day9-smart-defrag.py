import sys
from utils import input_utils
from tqdm.auto import tqdm


def expand_files(compacted: str) -> list[int | None]:
    expanded = list()
    for i in range(len(compacted)):
        expanded += [i] * int(compacted[i * 2])
        if i * 2 + 1 >= len(compacted):
            break
        expanded += [None] * int(compacted[i * 2 + 1])

    return expanded


def find_first_fitting_space(defragged: list[int | None], size: int) -> int | None:

    i = 0
    while i < len(defragged):
        if defragged[i] is not None:
            i += 1
            continue

        # found first space check ahead
        # print(f"found space at {i}", end=", ")
        j = i + 1
        while j < len(defragged) and (defragged[j] is None):
            j += 1
        size_space = j - i
        # print(f"ending at {j}, size {size_space}")

        if size_space >= size:
            return i
        else:
            i = max(i + 1, j)

    return None


def defrag(expanded: list[int | None], compacted) -> list[int | None]:
    fore = 0
    file_sizes = list()
    for i in range(len(compacted)):
        if i % 2 == 0:
            file_sizes.append(int(compacted[i]))

    defragged = expanded.copy()

    for file_id, file_size in tqdm(
        reversed(list(enumerate(file_sizes))), total=len(file_sizes)
    ):
        # print("file", file_id, "size", file_size)
        move_to = find_first_fitting_space(defragged, file_size)
        start_file = defragged.index(file_id)
        # print(f"fitting space idx: {move_to}, file start: {start_file}")
        if move_to is not None and move_to < start_file:
            # print("will move")
            for i in range(file_size):
                # erase file to be moved #IMPROVE ME!!!
                defragged[start_file + i] = None
                # write file
                defragged[move_to + i] = file_id

            # print(defragged)

    return defragged


def checksum(defragged: str) -> int:
    result = 0
    for i, c in enumerate(defragged):
        if c is None:
            continue
        result += i * int(c)
    return result


def main() -> int:
    input_str = input_utils.get_input_lines_from_args()[0]
    # print(input_str)
    expanded = expand_files(input_str)
    # print(expanded)
    defragged = defrag(expanded, input_str)
    # print(defragged)
    print(checksum(defragged))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
