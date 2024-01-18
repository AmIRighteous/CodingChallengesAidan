import sys
from enum import Enum


class STD(Enum):
    IN = "STDIN"
    OUT = "STDOUT"


def parse_cli(args: list[str]) -> dict:
    flags = {"input": [], "count_lines": False, "exclude_line_breaks": False}
    for arg in args:
        if arg == "cccat.py":
            continue
        elif arg.endswith(".txt"):
            flags["input"].append(arg)
        elif arg == "-n":
            flags["count_lines"] = True
        elif arg == "-b":
            flags["count_lines"] = True
            flags["exclude_line_breaks"] = True
        elif arg == "-":
            flags["input"] = STD.IN
    return flags


def fetch_input(input_flag) -> list:
    if input_flag == STD.IN:
        contents = "".join(sys.stdin.readlines())
    elif isinstance(input_flag, str):
        with open(input_flag, "r", encoding="utf-8") as f:
            contents = f.read()
    elif isinstance(input_flag, list):
        contents = ""
        for file_name in input_flag:
            with open(file_name, "r", encoding="utf-8") as f:
                contents += f.read()
            contents += "\n"
    return contents


def write_output(flags: dict, data):
    if not flags["count_lines"]:
        print(data, end="")
    else:
        lines = data.split("\n")
        if not flags["exclude_line_breaks"]:
            for i in range(len(lines) - 1):
                print(f"{i + 1} {lines[i]}")
        else:
            counter = 1
            for i in range(len(lines) - 1):
                if lines[i] == "":
                    print("")
                else:
                    print(f"{counter} {lines[i]}")
                    counter += 1


if __name__ == "__main__":
    flags = parse_cli(sys.argv)
    input = fetch_input(flags["input"])
    write_output(flags, input)
