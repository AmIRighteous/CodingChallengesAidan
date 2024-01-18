# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
import os
import re

parser = argparse.ArgumentParser()

parser.add_argument("-c", help="Byte Count of File")
parser.add_argument("-l", help="Line Count of File")
parser.add_argument("-w", help="Word Count of File")
parser.add_argument("-m", help="Char Count of File")

args = parser.parse_args()


def get_bytes(file_path: str) -> int:
    try:
        size = os.path.getsize(file_path)
        return size
    except FileNotFoundError:
        print(f"File not Found: {file_path}")
        return -1


def get_lines(file_path: str) -> int:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            line_count = sum(1 for line in f)
            return line_count
    except FileNotFoundError:
        print(f"File not Found: {file_path}")
        return -1


def get_words(file_path: str) -> int:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        prime = re.sub(r"\s+", " ", file_content)
        modded = prime.strip().replace("\t", " ").replace("\n", " ").split()
        return len(modded)
    except FileNotFoundError:
        print(f"File not Found: {file_path}")
        return -1


def get_chars(file_path: str) -> int:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        chars = 0
        for char in file_content:
            if char == "\n":
                chars += 2
            else:
                chars += 1
        return chars
    except FileNotFoundError:
        print(f"File not Found: {file_path}")
        return -1


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.
    output = ""
    if args.c:
        output = str(get_bytes(args.c)) + " " + args.c
    elif args.l:
        output = str(get_lines(args.l)) + " " + args.l
    elif args.w:
        output = str(get_words(args.w)) + " " + args.w
    elif args.m:
        output = str(get_chars(args.m)) + " " + args.m

    print(output)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_hi("Aidan")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
