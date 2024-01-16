import pytest

from src.ccsort.ccsort import (
    parse_cli,
    SORT,
    sort_coordinator,
    fetch_input,
    STD,
    filter_for_uniques,
)


@pytest.mark.parametrize(
    "sys_argv, expected_result",
    [
        (
            ["ccsort.py", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.MERGE,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "text.txt", "output.txt"],
            {
                "input": "text.txt",
                "output": "output.txt",
                "unique": False,
                "sort": SORT.MERGE,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-t", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.MERGE,
                "timer": True,
            },
        ),
        (
            ["ccsort.py", "-u", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": True,
                "sort": SORT.MERGE,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-radix-sort", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.RADIX,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-sort=radix", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.RADIX,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-merge-sort", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.MERGE,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-sort=merge", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.MERGE,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-quick-sort", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.QUICK,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-sort=quick", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.QUICK,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-heap-sort", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.HEAP,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-sort=heap", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.HEAP,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-heap-sort", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.HEAP,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-R", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.RANDOM,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-random-sort", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.RANDOM,
                "timer": False,
            },
        ),
        (
            ["ccsort.py", "-sort=random", "text.txt"],
            {
                "input": "text.txt",
                "output": STD.OUT,
                "unique": False,
                "sort": SORT.RANDOM,
                "timer": False,
            },
        ),
    ],
)
def test_parse_cli(sys_argv, expected_result):
    flags = parse_cli(sys_argv)
    assert flags == expected_result


@pytest.mark.parametrize(
    "sort_type, pre_sort, post_sort",
    [
        (SORT.MERGE, ["B", "C", "A"], ["A", "B", "C"]),
        (SORT.HEAP, ["B", "C", "A"], ["A", "B", "C"]),
        (SORT.RADIX, ["B", "C", "A"], ["A", "B", "C"]),
        (SORT.QUICK, ["B", "C", "A"], ["A", "B", "C"]),
    ],
)
def test_sorting_algos(sort_type, pre_sort, post_sort):
    actual = sort_coordinator(pre_sort, sort_type)
    assert actual == post_sort


def test_random_sort():
    input = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    output1 = sort_coordinator(input, SORT.RANDOM)
    assert input != output1
    output2 = sort_coordinator(input, SORT.RANDOM)
    assert output1 != output2


@pytest.mark.parametrize(
    "input_file, expected_output",
    [
        ("test.txt", ["B", "C", "A", "D", "E", "F", "G", "H", "I"]),
        (
            "shorter_words.txt",
            [
                "The",
                "Project",
                "Gutenberg",
                "eBook",
                "of",
                "The",
                "Art",
                "of",
                "War",
                "This",
            ],
        ),
    ],
)
def test_read_input(input_file, expected_output):
    flags = {"input": input_file}
    actual_output = fetch_input(flags)
    assert expected_output == actual_output


@pytest.mark.parametrize(
    "input, expected_output", [(["a", "a", "b"], ["a", "b"])]
)  # TODO add more testcases
def test_for_uniques(input, expected_output):
    actual = filter_for_uniques(input)
    assert sorted(actual) == expected_output
