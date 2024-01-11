import sys
from enum import Enum
"""
    1. Sketch out the vision - what is the application going to do at a high level.
    -read input file, compare adjacent lines for duplicates, only writes unique lines to output file
    -if no input file or input file is single dash `-`, read from stdin
    -if no output file, write to stdout
    -repeat lines in input aren't detected if not adjacent, so may need to sort files first
    - -c or --count command keeps track of how many times the line was present in the input
    - -d or --repeated should output only the lines that were repeated
    - -u only prints out unique lines
    - support for -c -d


    2. Break down the application into building blocks
    -parser of cli arguments
    -read data (stdin or input file), probs into a dict with occurrences, return output
    -function that takes data and puts in stdout or file

    3. Build the core of one or more of the fundamental blocks using test driven development.

    4. Build a walking skeleton - once I’ve built any fundamental blocks, I like to build a walking skeleton.
    A walking skeleton is a tiny implementation of a system that performs a very small end-to-end function.

    5. Flesh out the functionality - Once I have a walking skeleton I start to add flesh to it. Adding more end-to-end slices of functionality by writing tests and then the code to pass them, for the minimum functionality I will need for each block, to deliver the end-to-end slice. Repeat until all the functionality is there.

    6. Refactor - This isn’t really step 6, I tend to refactor as I go.
    As the software evolves I will have to change things that were done to enable the development of a walking skeleton
"""


class STD(Enum):
    IN = "STDIN"
    OUT = "STDOUT"


def parse_cli(args: list[str]) -> dict:
    flags = {"output_mods": []}
    for arg in args:
        if arg == "ccuniq.py":
            continue
        elif arg == "-":
            flags["input"] = STD.IN
        elif arg.endswith(".txt"):
            if "input" in flags:
                flags["output"] = arg
            else:
                flags["input"] = arg
        elif arg == "-c" or arg == "--count":
            flags["output_mods"].append("c")
        elif arg == "-u":
            flags["output_mods"].append("u")
        elif arg == "-d" or arg == "--repeated":
            flags["output_mods"].append("d")
    if "input" not in flags:
        flags["input"] = STD.IN
    if "output" not in flags:
        flags["output"] = STD.OUT

    return flags


def parse_normal(lines: list) -> str:
    prev_line = lines[0]
    uniq_lines = prev_line
    for i in range(1, len(lines)):
        line = lines[i]
        if line != prev_line:
            uniq_lines += line
            prev_line = line
    return uniq_lines


def parse_count_lines(lines: list, repeated: bool = False) -> str:
    data = {"lines": [], "line_count": {}}
    for i in range(len(lines)):
        line = lines[i]
        if line in data["lines"]:
            data["line_count"][line] += 1
        else:
            data["lines"].append(line)
            data["line_count"][line] = 1
    temp = ""
    for line in data["lines"]:
        if (repeated and data["line_count"][line] > 1) or not repeated:
            temp += str(data["line_count"][line]) + " " + line
    return temp


def parse_repeated_lines(lines: list) -> str:
    out = ""
    count_lines = []
    found_repeats = set()
    prev_line = lines[0]
    for i in range(1, len(lines)):
        line = lines[i]
        if line == prev_line and line not in found_repeats:
            found_repeats.add(line)
            out += line
            count_lines.append(line)
        prev_line = line
    return out


def parse_unique_lines(lines: list) -> str:
    temp = []
    seen = set()
    for i in range(len(lines)):
        line = lines[i]
        if line not in seen:
            temp.append(line)
            seen.add(line)
        elif line in temp:
            temp = list(filter(lambda x: x != line, temp))

    return "".join(temp)


if __name__ == '__main__':
    output = ""
    flags = parse_cli(sys.argv)
    if flags["input"] != STD.IN:
        with open(flags["input"], "r", encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()
    if len(flags["output_mods"]) == 0:
        output = parse_normal(lines)
    elif len(flags["output_mods"]) == 1:
        mod = flags["output_mods"][0]
        if mod == "c":
            output = parse_count_lines(lines)
        elif mod == "d":
            output = parse_repeated_lines(lines)
        elif mod == "u":
            output = parse_unique_lines(lines)
    elif len(flags["output_mods"]) == 2:
        output = parse_count_lines(lines, repeated=True)
    if flags["output"] != STD.OUT:
        with open(flags["output"], "w") as f:
            f.write(output)
    else:
        print(output, end='')