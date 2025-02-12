from utils.input_utils import get_input_lines_from_args, str_seq_to_int_tup
import math
from tqdm import tqdm


def parse_one_number(num: int) -> list[int, ...]:

    # If the stone is engraved with the number 0, it is replaced by a
    # stone engraved with the number 1.
    if num == 0:
        return [1]
    # If the stone is engraved with a number that has an even number of
    # digits, it is replaced by two stones. The left half of the digits
    # are engraved on the new left stone, and the right half of the
    # digits are engraved on the new right stone. (The new numbers don't
    # keep extra leading zeroes: 1000 would become stones 10 and 0.)
    str_num = str(num)
    digits = int(math.log10(num)) + 1
    if digits % 2 == 0:
        left = int(str_num[: int(digits / 2)])
        right = int(str_num[int(digits / 2) :])
        return [left, right]

    # If none of the other rules apply, the stone is replaced by a new stone;
    # the old stone's number multiplied by 2024 is engraved on the new stone.
    return [num * 2024]


def main() -> int:
    line = get_input_lines_from_args()[0]
    line = list(str_seq_to_int_tup(line, " "))

    for i in tqdm(range(1, 26)):
        # print(i)
        # print(line)
        new_line = []
        for num in line:
            # print(f"parsing {num}: {parse_one_number(num)}")
            new_line.extend(parse_one_number(num))

        # input(str(new_line))
        line = new_line
    print(len(line))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
