import sys
from utils import input_utils


def expand_files(compacted: str) -> list[int]:
    expanded = list()
    for i in range(len(compacted)):
        expanded += [i] * int(compacted[i * 2])
        if i * 2 + 1 >= len(compacted):
            break
        expanded += ["."] * int(compacted[i * 2 + 1])

    return expanded


def swap_str_char(s: str, pos1: int, pos2: int) -> str:
    if pos1 == pos2:
        return s  # derp
    # ensure pos1 <= pos2
    if pos2 < pos1:
        pos1, pos2 = pos2, pos1
    p1 = s[pos1]
    p2 = s[pos2]
    new_str = s[:pos1] + p2 + s[pos1 + 1 : pos2] + p1 + s[pos2 + 1 :]

    return new_str


def swap(s: list, pos1: int, pos2: int) -> None:
    if pos2 <= pos1:
        return
    # mutates s
    if pos1 == pos2:
        return  # derp
    p1 = s[pos1]
    s[pos1] = s[pos2]
    s[pos2] = p1


def defrag(expanded: str) -> str:
    fore = 0
    back = len(expanded) - 1

    defragged = expanded.copy()
    while fore < back:
        if defragged[fore] == ".":
            while defragged[back] == ".":
                back -= 1
            swap(defragged, fore, back)
        # print(f"{defragged}   ({fore},{back})")
        fore += 1

    return defragged


def checksum(defragged: str) -> int:
    result = 0
    for i, c in enumerate(defragged):
        if c == ".":
            return result
        result += i * int(c)
    return result


def main() -> int:
    input_str = input_utils.get_input_lines_from_args()[0]
    # print(input_str)
    expanded = expand_files(input_str)
    # print(expanded)
    defragged = defrag(expanded)
    print(defragged)
    print(checksum(defragged))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
