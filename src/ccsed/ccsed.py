# parse input
# parse cli instructions
# apply cli instructions to input
# output result
import sys
from enum import Enum


class STD(Enum):
    IN = "STDIN"
    OUT = "STDOUT"


def parse_cli(args):
    cli_args = {
        "input": STD.IN,
        "double_space": False,
        "regex_swaps": {},
        "regex_keys": [],
        "lines": [],
        "output": STD.OUT,
    }
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "ccsed.py" or arg == "python":
            i += 1
            continue
        elif arg.endswith(".txt"):
            cli_args["input"] = arg
        elif arg == "G":
            cli_args["double_space"] = True
        elif arg.startswith("s/"):
            spliced = arg.split("/")
            pre, post = spliced[1], spliced[-2]
            cli_args["regex_swaps"][pre] = post
        elif arg == "-n":
            next_arg = args[i + 1]
            if next_arg.endswith("/p"):
                k = next_arg.split("/")[1]
                cli_args["regex_keys"].append(k)
            else:
                temp = next_arg.split(",")
                start, stop, = int(
                    temp[0]
                ), int(temp[1][0])
                cli_args["lines"] = [start, stop]
            i += 1
        elif arg == "-i":
            cli_args["output"] = "REPLACE"
        i += 1
    if cli_args["output"] == "REPLACE" and cli_args["input"] != STD.IN:
        cli_args["output"] = cli_args["input"]

    return cli_args


def fetch_input(input_flag) -> list:
    if input_flag == STD.IN:
        contents = "".join(sys.stdin.readlines())
    else:
        with open(input_flag, "r", encoding="utf-8") as f:
            contents = f.read()
    return contents


if __name__ == "__main__":
    flags = parse_cli(sys.argv)
    input = fetch_input(flags["input"])
