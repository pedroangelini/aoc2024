import sys


def get_input_lines_from_args() -> list[str]:
    try:
        with open(sys.argv[1], "r", encoding="utf8") as fp:
            lines = fp.read().rstrip("\n").split("\n")
    except Exception as e:  # IndexError, FileNotFound
        print(f"Error {type(e).__name__} -> {str(e)}")
        print(f"Usage: python {sys.argv[0]} input-file.txt")
        raise SystemExit(1)

    return lines
