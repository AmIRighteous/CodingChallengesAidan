import string
import sys
import re

special_commands: dict[str] = {
    "[:alnum:]": [chr(i) for i in range(33, 127) if chr(i).isalnum()],
    "[:alpha:]": [chr(ord(i)) for i in string.ascii_letters],
    "[:blank:]": ['\x09', '\x20'],
    "[:cntrl:]": ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f'],
    "[:digit:]": [1,2,3,4,5,6,7,8,9,0],
    "[:lower:]": [chr(ord(i)) for i in string.ascii_lowercase],
    "[:print:]": [chr(i) for i in range(32, 127)],
    "[:punct:]": [chr(i) for i in range(33, 127) if chr(i).isprintable() and chr(i).isspace() == False and chr(i).isalnum() == False],
    "[:space:]": [chr(i) for i in range(128) if chr(i).isspace()],
    "[:upper:]": [chr(ord(i)) for i in string.ascii_uppercase],
}


def get_char_list(set: str)-> list[str]:
    if len(set) == 1:
        return [set]
    elif set in special_commands:
        return special_commands[set]
    else:
        return [chr(i) for i in range(ord(set[0]), ord(set[2])+1)]


def generate_sub_mappings(from_set: str, to_set: str)->dict[str]:
    from_list = get_char_list(from_set)
    to_list = get_char_list(to_set)
    error_msg = ""
    if len(from_list) < len(to_list):
        error_msg = "ERROR, from_list smaller than to_list, impossible to map from->to, ending now"
    elif len(from_list) == len(to_list):
        return dict(zip(from_list, to_list))
    elif len(from_list) > len(to_list) and len(to_list) == 1:
        return {from_list[i]: to_list[0] for i in range(len(from_list))}
    elif len(from_list) > len(to_list):
        error_msg = "to_list smaller than from_list, but to_list is not of length 1, thus unmappable"
    else:
        error_msg = f"UNEXPECTED ERROR, from_list: {from_list} | to_list: {to_list}"
    raise Exception(error_msg)


def generate_del_mappings(deleted_chars: str) -> dict[str]:
    if deleted_chars.strip('"') in special_commands:
        return {i: "" for i in special_commands[deleted_chars.strip('"')]}
    return {deleted_chars[i]: "" for i in range(len(deleted_chars))}


def tr_driver() -> None:
    arg_1 = sys.argv[1]
    arg_2 = sys.argv[2]
    standard_in = sys.stdin.read()
    if arg_1 == "-s":
        pattern = re.compile(rf'({"|".join(re.escape(char) for char in get_char_list(arg_2))})\1+')
        result = pattern.sub(lambda x: x.group(1), standard_in)
        print(result)
    elif arg_1 == "-ds":
        # delete first, then squash
        ...
    else:
        if arg_1 == "-d":
            char_mappings = generate_del_mappings(arg_2)
        else:
            char_mappings = generate_sub_mappings(arg_1, arg_2)
        keys = [re.escape(k) for k in char_mappings.keys()]
        pattern = '|'.join(sorted(keys))
        result = re.sub(pattern, lambda x: char_mappings.get(x.group(0)), standard_in)
        print(result)
    return


if __name__ == '__main__':
    tr_driver()
