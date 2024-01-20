import pytest

from src.ccsed.ccsed import parse_cli, STD, runner


@pytest.mark.parametrize(
    "sys_argv, expected_result",
    [
        (
            ["python", "ccsed.py", "s/this/that/g", "test.txt"],
            {
                "input": "test.txt",
                "double_space": False,
                "regex_swaps": {"this": "that"},
                "regex_keys": "",
                "lines": [],
                "output": STD.OUT,
            },
        ),
        (
            ["python", "ccsed.py", "-n", "2,4p"],
            {
                "input": STD.IN,
                "double_space": False,
                "regex_swaps": {},
                "regex_keys": "",
                "lines": [2, 4],
                "output": STD.OUT,
            },
        ),
        (
            ["python", "ccsed.py", "-n", "/roads/p", "test.txt"],
            {
                "input": "test.txt",
                "double_space": False,
                "regex_swaps": {},
                "regex_keys": "roads",
                "lines": [],
                "output": STD.OUT,
            },
        ),
        (
            ["python", "ccsed.py", "G", "test.txt"],
            {
                "input": "test.txt",
                "double_space": True,
                "regex_swaps": {},
                "regex_keys": "",
                "lines": [],
                "output": STD.OUT,
            },
        ),
        (
            ["python", "ccsed.py", "-i", "s/Life/Code/g", "test.txt"],
            {
                "input": "test.txt",
                "double_space": False,
                "regex_swaps": {"Life": "Code"},
                "regex_keys": "",
                "lines": [],
                "output": "test.txt",
            },
        ),
    ],
)
def test_parse_cli(sys_argv, expected_result):
    flags = parse_cli(sys_argv)
    assert flags == expected_result


@pytest.mark.parametrize("sys_argv", [(["ccsed.py", "-n", "/roads/p", "test.txt"])])
def test_runner(sys_argv):
    runner(sys_argv)
