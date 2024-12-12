from utils import input_utils
from collections import defaultdict


def main() -> int:
    lines = input_utils.get_input_lines_from_args()
    list1 = []
    list2 = []
    for l in lines:
        i1, i2 = l.split()
        list1.append(int(i1))
        list2.append(int(i2))

    counter_list2 = defaultdict(int)
    for i in list2:
        counter_list2[i] += 1

    total = 0
    for i in list1:

        total += i * counter_list2[i]

    print(f"{total = }")


if __name__ == "__main__":
    raise SystemExit(main())
