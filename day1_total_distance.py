import sys
from utils import input_utils


def main() -> int:
    lines = input_utils.get_input_lines_from_args()
    list1 = []
    list2 = []
    for l in lines:
        i1, i2 = l.split()
        list1.append(int(i1))
        list2.append(int(i2))

    list1.sort()
    list2.sort()

    total = sum([abs(i[0] - i[1]) for i in zip(list1, list2)])
    print(total)


if __name__ == "__main__":
    raise SystemExit(main())
