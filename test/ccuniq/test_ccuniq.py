import pytest

from src.ccuniq.ccuniq import parse_cli, STD, parse_input


@pytest.mark.parametrize("sys_argv, expected_result", [
    (["ccuniq.py", "test.txt"], {"input": "test.txt", "output": STD.OUT, "output_mods": []}),
    (["ccuniq.py", "test.txt", "test_output.txt"], {"input": "test.txt", "output": "test_output.txt", "output_mods": []}),
    (["ccuniq.py"], {"input": STD.IN, "output": STD.OUT, "output_mods": []}),
    (["ccuniq.py", "-"], {"input": STD.IN, "output": STD.OUT, "output_mods": []}),
    (["ccuniq.py", "-", "output.txt"], {"input": STD.IN, "output": "output.txt", "output_mods": []}),
    (["ccuniq.py", "-c", "test.txt"], {"input": "test.txt", "output": STD.OUT, "output_mods": ["c"]}),
    (["ccuniq.py", "--count", "test.txt"], {"input": "test.txt", "output": STD.OUT, "output_mods": ["c"]}),
    (["ccuniq.py", "-d", "test.txt"], {"input": "test.txt", "output": STD.OUT, "output_mods": ["d"]}),
    (["ccuniq.py", "--repeated", "test.txt"], {"input": "test.txt", "output": STD.OUT, "output_mods": ["d"]}),
    (["ccuniq.py", "-u", "test.txt"], {"input": "test.txt", "output": STD.OUT, "output_mods": ["u"]}),
    (["ccuniq.py", "-d", "-c", "test.txt"], {"input": "test.txt", "output": STD.OUT, "output_mods": ["d", "c"]}),
    (["ccuniq.py", "-c", "-d", "test.txt"], {"input": "test.txt", "output": STD.OUT, "output_mods": ["c", "d"]}),
    (["ccuniq.py", "-c", "-u", "test.txt"], {"input": "test.txt", "output": STD.OUT, "output_mods": ["c", "u"]}),
])
def test_parse_cli(sys_argv, expected_result):
    flags = parse_cli(sys_argv)
    assert flags == expected_result

@pytest.mark.parametrize("flags, expected_output", [
    ({"input": "test.txt", "output": STD.OUT, "output_mods": []}, {"line1": 1, "line2": 2, "line3": 1, "line4": 1})
])
def test_parse_input(flags, expected_output):
    lines_nums = parse_input(flags)
    assert lines_nums == expected_output