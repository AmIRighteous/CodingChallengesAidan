"""
    1. Sketch out the vision - what is the application going to do at a high level.
    -In this case we want to build a tool that can cut out selected portions from each line in a file

    2. Break down the application into building blocks
    -block that takes in CLI arguments to understand what the user wants
    -block that reads the file we want to slice from
    -block that extracts proper data from file, given CLI args

    3. Build the core of one or more of the fundamental blocks using test driven development.

    4. Build a walking skeleton - once I’ve built any fundamental blocks, I like to build a walking skeleton. A walking skeleton is a tiny implementation of a system that performs a very small end-to-end function. For the Redis clone that might be building just enough to handle a client connection request, parsing an incoming message and handling the simplest possible command: PING.

    5. Flesh out the functionality - Once I have a walking skeleton I start to add flesh to it. Adding more end-to-end slices of functionality by writing tests and then the code to pass them, for the minimum functionality I will need for each block, to deliver the end-to-end slice. Repeat until all the functionality is there.

    6. Refactor - This isn’t really step 6, I tend to refactor as I go. As the software evolves I will have to change things that were done to enable the development of a walking skeleton (i.e. I might not handle concurrent clients when I handle PING). I will also refactor as I gain a better understanding of the challenges and my design evolves.
"""


def parse_cli(args: list[str]) -> dict:
    """
    Needs to be able to handle the following variations:
    -Fieldnames:
        -[field_name]
        -[field_prefix][field_id],[field_id]
        -[field_prefix]"[field_id] [field_id]..."
    -Delimiters
        -d[delimiter]
    -Filename
        [filename]
        - && (nothing) -> both pull from std in

    :param args: system arguments, taking in as a list rather than reading directly from sys.argv for easier testing
    :return: a dictionary that will contain the instructions about how we want to cut the information
    """
    flags = {"delimiter": "\t"}
    for arg in args:
        if arg.startswith("-d"):
            flags["delimiter"] = arg[2:]
        elif arg.startswith("-f"):
            if "," in arg:
                flags["columns"] = [int(x) for x in arg[2:].split(",")]
            elif '"' in arg:
                flags["columns"] = [int(x) for x in arg[3:-1].split(" ")]
            else:
                flags["columns"] = [int(arg[2:])]
        elif "cccut.py" in arg:
            continue
        elif arg == "-":
            flags["stdin"] = True
        else:
            flags["file_name"] = arg
    if "file_name" not in flags:
        flags["stdin"] = True
    return flags


def hello_world() -> None:
    print("hello world")


if __name__ == '__main__':
    hello_world()