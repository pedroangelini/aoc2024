from utils import input_utils
from itertools import pairwise
import rich


def check_safe(list_input: list[int]) -> bool:
    # print(list_input)
    if list_input[1] > list_input[0]:
        ascending = True
    elif list_input[1] < list_input[0]:
        ascending = False
    else:
        # print("fail - first 2 items equal")
        # input()
        return False

    for a, b in pairwise(list_input):
        dist = abs(a - b)
        # print(a, b, f"{ascending=}", f"{dist=}")
        if ascending and a < b and (1 <= dist <= 3):
            continue
        elif not ascending and a > b and (1 <= dist <= 3):
            continue
        else:
            # print("unsafe")
            # input()
            return False
    # print("safe")
    # input()
    return True


def main() -> int:
    reports = input_utils.get_input_lines_from_args()

    safe_count = 0
    for report in reports:
        report = [int(n) for n in report.split()]
        # print("------")
        if check_safe(report):
            safe_count += 1
            continue
        for i in range(len(report)):
            sanitized = report.copy()
            del sanitized[i]
            if check_safe(sanitized):
                safe_count += 1
                break

    # rich.print(list(zip(reports, safe_check)))
    print(safe_count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
