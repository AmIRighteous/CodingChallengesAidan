"""
    1. Sketch out the vision - what is the application going to do at a high level.
    -general sort that just sorts lexicographically via opening a file & dumping to STDOUT
    - -u removes all duplicate lines in the file (maybe have a set that holds all the words that exist, as well as a list?)
    - -[radix/merge/quick/heap]-sort or -sort=[radix/merge/quick/heap]
    - R or -random-sort or -sort=random for random sorting
    - if there's a second file included then write output to that file

    2. Break down the application into building blocks
    -CLI parser obvy
    -flag

    3. Build the core of one or more of the fundamental blocks using test driven development.

    4. Build a walking skeleton - once I’ve built any fundamental blocks, I like to build a walking skeleton.
    A walking skeleton is a tiny implementation of a system that performs a very small end-to-end function.

    5. Flesh out the functionality - Once I have a walking skeleton I start to add flesh to it. Adding more end-to-end slices of functionality by writing tests and then the code to pass them, for the minimum functionality I will need for each block, to deliver the end-to-end slice. Repeat until all the functionality is there.

    6. Refactor - This isn’t really step 6, I tend to refactor as I go.
    As the software evolves I will have to change things that were done to enable the development of a walking skeleton
"""
import re
import sys
import timeit
from enum import Enum
import random


class STD(Enum):
    IN = "STDIN"
    OUT = "STDOUT"


class SORT(Enum):
    RADIX = "RADIX"
    MERGE = "MERGE"
    QUICK = "QUICK"
    HEAP = "HEAP"
    RANDOM = "RANDOM"


def parse_cli(args: list[str]) -> dict:
    flags = {
        "input": STD.IN,
        "output": STD.OUT,
        "unique": False,
        "sort": SORT.QUICK,
        "timer": False,
    }
    for arg in args:
        if arg == "ccsort.py":
            continue
        elif arg.endswith(".txt"):
            if flags["input"] == STD.IN:
                flags["input"] = arg
            else:
                flags["output"] = arg
        elif arg == "-u":
            flags["unique"] = True
        elif "sort" in arg:
            if "merge" in arg:
                flags["sort"] = SORT.MERGE
            elif "quick" in arg:
                flags["sort"] = SORT.QUICK
            elif "heap" in arg:
                flags["sort"] = SORT.HEAP
            elif "radix" in arg:
                flags["sort"] = SORT.RADIX
            elif "random" in arg:
                flags["sort"] = SORT.RANDOM
        elif arg == "-r" or arg == "-R":
            flags["sort"] = SORT.RANDOM
        elif arg == "-t":
            flags["timer"] = True
    return flags


def merge_sort(data: list) -> list:
    def merge_helper(arr: list) -> list:
        if len(arr) > 1:
            mid = len(arr) // 2
            L, R = arr[:mid], arr[mid:]
            merge_helper(L)
            merge_helper(R)
            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
            while i < len(L):
                arr[k] = L[i]
                k += 1
                i += 1
            while j < len(R):
                arr[k] = R[j]
                k += 1
                j += 1
        return arr

    result = merge_helper(data)
    return result


def heap_sort(data):
    def heap_helper(arr, N, i):
        largest = i  # init largest as root
        l = 2 * i + 1  # set left and right values based on array pos
        r = 2 * i + 2
        # check if left of root exists and is greater than root
        if l < N and arr[largest] < arr[l]:
            largest = l
        # check if right child exists and is greater than root
        if r < N and arr[largest] < arr[r]:
            largest = r
        # update root if needed
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]  # make the swap
            heap_helper(arr, N, largest)  # heapify root

    N = len(data)
    # build the maxheap
    for i in range(N // 2 - 1, -1, -1):
        heap_helper(data, N, i)
    sorted_arr = []
    # pull elements 1-by-1
    for i in range(N - 1, 0, -1):
        data[i], data[0] = data[0], data[i]  # swap
        sorted_arr.insert(0, data.pop())
        heap_helper(data, i, 0)
    sorted_arr.insert(0, data[0])
    return sorted_arr


def radix_sort(data):
    n = len(data)

    def radix_helper(arr, n, place):
        output = [""] * n
        count = [0] * 256
        for i in range(n):  # store count of occurences in count
            ind = ord(arr[i][place]) if len(arr[i]) > place else 0
            count[ind] += 1
        # change count[i] such that it now contains actual position of this digit in the output array
        for i in range(1, 256):
            count[i] += count[i - 1]
        # build output array
        i = n - 1
        while i >= 0:
            ind = ord(arr[i][place]) if len(arr[i]) > place else 0
            output[count[ind] - 1] = arr[i]
            count[ind] -= 1
            i -= 1
        # return output
        return output

    if isinstance(data[0], int):
        max_len = max(data)
    else:
        max_len = max(len(s) for s in data)

    # do count sorting for every char in string
    for exp in range(max_len - 1, -1, -1):
        data = radix_helper(data, n, exp)
    return data


def quick_sort(data):
    def find_partition(arr, l, r):
        pivot = arr[r]
        i = l - 1
        for j in range(l, r):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[r] = arr[r], arr[i + 1]
        return i + 1

    def quick_helper(arr, l, r):
        if l < r:
            pi = find_partition(arr, l, r)
            quick_helper(arr, l, pi - 1)
            quick_helper(arr, pi + 1, r)
        return arr

    n = len(data)
    return quick_helper(data, 0, n - 1)


def random_sort(data):
    occ_by_word = {}
    for word in data:
        if word in occ_by_word:
            occ_by_word[word] += 1
        else:
            occ_by_word[word] = 1
    output = []
    keys = list(occ_by_word.keys())
    random.shuffle(keys)
    for k in keys:
        temp = [k] * occ_by_word[k]
        output.extend(temp)
    return output


def filter_for_uniques(data):
    s = set()
    for piece in data:
        if piece not in s:
            s.add(piece)
    return list(s)


def sort_coordinator(data, sort_type, unique=False):
    print("Using sort type:", sort_type.value)
    if unique:
        data = filter_for_uniques(data)
    if sort_type == SORT.MERGE:
        output = merge_sort(data)
    elif sort_type == SORT.QUICK:
        output = quick_sort(data)
    elif sort_type == SORT.RADIX:
        output = radix_sort(data)
    elif sort_type == SORT.HEAP:
        output = heap_sort(data)
    elif sort_type == SORT.RANDOM:
        output = random_sort(data)
    else:
        raise Exception(
            f"ERROR: Sort type {sort_type} not matched to known sorting function."
        )
    return output


def time_test(input):
    timeit.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
    """
    merge_str = f"""merge_sort({input})"""
    merge = timeit.Timer(
        stmt=merge_str,
        setup="from __main__ import merge_sort",
    )
    radix_str = f"""radix_sort({input})"""
    radix = timeit.Timer(
        stmt=radix_str,
        setup="from __main__ import radix_sort",
    )
    heap_str = f"""heap_sort({input})"""
    heap = timeit.Timer(
        stmt=heap_str,
        setup="from __main__ import heap_sort",
    )
    quick_str = f"""quick_sort({input})"""
    quick = timeit.Timer(
        stmt=quick_str,
        setup="from __main__ import quick_sort",
    )
    vals = merge.timeit(1000)
    times = {
        SORT.MERGE: vals[0],
        SORT.RADIX: radix.timeit(1000)[0],
        SORT.HEAP: heap.timeit(1000)[0],
        SORT.QUICK: quick.timeit(1000)[0],
    }
    return vals[1], times


def fetch_input(input_flag) -> list:
    if input_flag == STD.IN:
        contents = "".join(sys.stdin.readlines())
    else:
        with open(input_flag, "r", encoding="utf-8") as f:
            contents = f.read()
    prime = re.sub(r"\s", " ", contents)
    words = prime.strip().replace("\t", " ").replace("\n", " ").split()
    return words


if __name__ == "__main__":
    flags = parse_cli(sys.argv)
    input = fetch_input(flags["input"])
    if flags["timer"]:
        output, times = time_test(input)
        for sort, time in times.items():
            print(f"{sort.value}: {time}")
    else:
        output = sort_coordinator(input, flags["sort"], flags["unique"])
    if flags["output"] == STD.OUT:
        print("\n".join(output))
    else:
        with open(flags["output"], "w") as f:
            for word in output:
                f.write(str(word) + "\n")
