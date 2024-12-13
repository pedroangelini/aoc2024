import re
from utils.input_utils import get_input_from_args, str_seq_to_int_tup

# import rich


def main() -> int:
    input = get_input_from_args()
    mult_matcher = re.compile(r"mul\((\d+),(\d+)\)")

    disabled_pat = re.compile(r"don\'t\(\)(?:.|\n)*?(?:do\(\)|$)")
    clean_input = disabled_pat.sub("", input)

    # rich.print(disabled_pat.findall(input))
    # print(input)
    # print(clean_input)

    acum = 0

    for match in mult_matcher.findall(clean_input):
        a, b = str_seq_to_int_tup(match)
        print(f"{a=}, {b=}, {(a*b)=}")
        acum += a * b

    print(acum)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
