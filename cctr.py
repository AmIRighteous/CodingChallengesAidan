import sys
import re


def generate_char_mappings(from_set: str, to_set: str)->dict[str]:
    if len(from_set) == 1 and len(to_set) == 1:
        return {from_set: to_set}
    elif "-" in from_set and "-" in to_set:
        from_list = [chr(i) for i in range(ord(from_set[0]), ord(from_set[2])+1)]
        to_list = [chr(i) for i in range(ord(to_set[0]), ord(to_set[2])+1)]
        return dict(zip(from_list, to_list))

def tr_driver()-> None:
    from_char = sys.argv[1]
    to_char = sys.argv[2]
    char_mappings = generate_char_mappings(from_char, to_char)
    keys = [re.escape(k) for k in char_mappings.keys()]
    pattern = '|'.join(sorted(keys))
    standard_in = sys.stdin.read()
    result = re.sub(pattern, lambda x: char_mappings.get(x.group(0)), standard_in)
    print(result)


if __name__ == '__main__':
    tr_driver()
