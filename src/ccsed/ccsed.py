import sys
import re
from enum import Enum


class STD(Enum):
    IN = "STDIN"
    OUT = "STDOUT"


def parse_cli(args):
    cli_args = {
        "input": STD.IN,
        "double_space": False,
        "regex_swaps": {},
        "regex_keys": "",
        "lines": [],
        "output": STD.OUT,
    }
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.endswith(".txt"):
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
                cli_args["regex_keys"] = k
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
    return contents.split("\n")


def filter_input(input, flags):
    prime = []
    if flags["regex_swaps"]:
        to = list(flags["regex_swaps"].keys())[0]
        fro = flags["regex_swaps"][to]
        for i in range(len(input)):
            prime.append(re.sub(to, fro, input[i]))
    elif flags["double_space"]:
        for i in range(len(input)):
            prime.append(input[i] + "\n")
    elif flags["regex_keys"]:
        patt = rf'^.*{re.escape(flags["regex_keys"])}.*$'
        for i in range(len(input)):
            if bool(re.match(patt, input[i])):
                prime.append(input[i])
    elif flags["lines"]:
        start, end = flags["lines"][0], flags["lines"][1]
        for i in range(start, end + 1):
            prime.append(f"{i}\t{input[i]}")
    return "\n".join(prime)


def runner(args):
    flags = parse_cli(args)
    input = fetch_input(flags["input"])
    output = filter_input(input, flags)
    if flags["output"] == STD.OUT:
        print(output, end="")
    else:
        with open(flags["output"], "w", encoding="utf-8") as f:
            f.write(output)


if __name__ == "__main__":
    runner(sys.argv)
