from utils.input_utils import get_input_from_args, str_seq_to_int_tup
import itertools
import sys


def check_update(update: tuple[int], rules: tuple[int]) -> bool:
    for comb in itertools.combinations(update, 2):
        if comb in rules:
            continue
        if (comb[1], comb[0]) in rules:
            return False
        else:
            print("should not have got here", file=sys.stderr)
            raise SystemExit(0)

    return True


def main() -> int:
    input = get_input_from_args()

    rules, updates = input.split("\n\n")

    rules = [str_seq_to_int_tup(rule, "|") for rule in rules.split("\n")]
    updates = [str_seq_to_int_tup(update, ",") for update in updates.split("\n")]

    # print(rules)
    # print(updates)

    acum: int = 0
    for update in updates:
        print(update, end=" ")
        if check_update(update, rules):
            acum += update[len(update) // 2]
            print("OK")
            continue
        print("NOK")

    print(f"result {acum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
