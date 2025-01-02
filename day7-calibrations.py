from utils.input_utils import get_input_lines_from_args, str_seq_to_int_tup
import itertools
from tqdm import tqdm

# from enum import Enum, auto


def concat(x: int, y: int):
    return int(str(x) + str(y))


operators = {"+": (lambda x, y: x + y), "*": (lambda x, y: x * y), "|": concat}


def check_eq_with_ops(equation: tuple, op_list: tuple) -> bool:
    # print(equation)

    eq_result = equation[0]

    if len(op_list) != (len(equation) - 2):
        raise ValueError(
            f"Equation and Operator length mismatch {equation=} ({len(equation)=}), {op_list=} ({len(op_list)=})"
        )
    running_result = equation[1]
    for pos in range(1, len(equation) - 1):
        op = operators[op_list[pos - 1]]
        # print(running_result, op_list[pos - 1], equation[pos + 1], end="")
        running_result = op(running_result, equation[pos + 1])
        # print(f" = {running_result}")

        # minor speed up since all numbers are positive
        if running_result > eq_result:
            return False

    return running_result == eq_result


def main() -> int:
    input = get_input_lines_from_args()
    # first value is the result
    equations = [str_seq_to_int_tup(l.replace(":", ""), " ") for l in input]

    running_result = 0
    for equation in tqdm(equations):
        for comb_operators in itertools.product("+*|", repeat=len(equation) - 2):
            # print(comb_operators)

            if check_eq_with_ops(equation, comb_operators):
                running_result += equation[0]
                break

    print()
    print(f"end result: {running_result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
