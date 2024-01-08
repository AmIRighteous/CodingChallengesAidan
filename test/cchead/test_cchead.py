import pytest

from src.cchead.cchead import parse_cli, read_file


@pytest.mark.parametrize("sys_argv, expected_result", [
    (["cchead.py", "test.txt"], {"lines": 10, "file_names": ["test.txt"]}),
    (["cchead.py"], {"lines": 10, "stdin": True}),
    (["cchead.py", "-n1"], {"lines": 1, "stdin": True}),
    (["cchead.py", "-n", "5"], {"lines": 5, "stdin": True}),
    (["cchead.py", "-n1", "test.txt"], {"lines": 1, "file_names": ["test.txt"]}),
    (["cchead.py", "-n", "10", "test.txt"], {"lines": 10, "file_names": ["test.txt"]}),
    (["cchead.py", "-n", "10", "test.txt", "test2.txt"], {"lines": 10, "file_names": ["test.txt", "test2.txt"]}),
])
def test_parse_cli(sys_argv, expected_result):
    flags = parse_cli(sys_argv)
    assert flags == expected_result


@pytest.mark.parametrize("flags, expected_data", [
    ({"lines": 1, "file_names": ["test.txt"]}, {"test.txt": "aaa\n"}),
    ({"chars": 1, "file_names": ["test.txt"]}, {"test.txt": "a"}),
    ({"chars": 3, "file_names": ["test.txt"]}, {"test.txt": "aaa"}),
    ({"chars": 50, "file_names": ["test.txt"]}, {"test.txt": "aaa\nbbb\nccc"}),
    ({"lines": 3, "file_names": ["test.txt"]}, {"test.txt": "aaa\nbbb\nccc"}),
    ({"lines": 10, "file_names": ["test.txt"]}, {"test.txt": "aaa\nbbb\nccc"}),
    ({"lines": 10, "file_names": ["small.txt"]}, {"test.txt": "aaa\nbbb\nccc"}),
])
def test_read_file(flags, expected_data):
    output = read_file(flags)
    assert output == expected_data