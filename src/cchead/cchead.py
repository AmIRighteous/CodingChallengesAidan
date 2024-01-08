import sys


def parse_cli(args: list[str]) -> dict:
    output = {"file_names": [], "lines": 10}
    index = 0
    while index < len(args):
        arg = args[index]
        if arg == "cchead.py":
            index += 1
            continue
        elif arg.startswith("-n"):
            if len(arg) > 2:
                output["lines"] = int(arg[2:])
                index += 1
            else:
                output["lines"] = int(args[index+1])
                index += 2
        elif arg.startswith("-c"):
            output.pop("lines")
            if len(arg) > 2:
                output["chars"] = int(arg[2:])
                index += 1
            else:
                output["chars"] = int(args[index+1])
                index += 2
        elif arg.endswith(".txt"):
            output["file_names"].append(arg)
            index += 1
    if len(output["file_names"]) == 0:
        output.pop("file_names")
        output["stdin"] = True
    return output


def read_file(flags: dict) -> dict:
    data = {}
    if "file_names" in flags:
        for file in flags["file_names"]:
            with open(file, "r", encoding='utf-8') as f:
                if "chars" in flags:
                    data[file] = f.read(flags["chars"])
                else:
                    i = 0
                    data[file] = ""
                    while i < flags["lines"]:
                        data[file] += f.readline()
                        i+= 1
    else:
        ...

    return data


if __name__ == '__main__':
    args = parse_cli(sys.argv)
    data = read_file(args)
    if len(data) == 1:
        for val in data.values():
            print(val)
    else:
        for title, info in data.items():
            print(f"==> {title} <==")
            print(info)