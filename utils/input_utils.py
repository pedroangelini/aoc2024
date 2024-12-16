import sys


def get_input_from_args() -> list[str]:
    try:
        with open(sys.argv[1], "r", encoding="utf8") as fp:
            input = fp.read().rstrip("\n")
    except Exception as e:  # IndexError, FileNotFound
        print(f"Error {type(e).__name__} -> {str(e)}")
        print(f"Usage: python {sys.argv[0]} input-file.txt")
        raise SystemExit(1)

    return input


def get_input_lines_from_args() -> list[str]:
    return get_input_from_args().split("\n")


def str_seq_to_int_tup(str_seq, sep: str | None = None) -> tuple[int]:
    if sep is None:
        return tuple(int(i) for i in str_seq)
    else:
        return tuple(int(i) for i in str_seq.split(sep))
