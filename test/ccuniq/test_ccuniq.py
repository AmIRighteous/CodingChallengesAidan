import pytest
from src.shared_components import STD
from src.ccuniq.ccuniq import parse_cli


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
