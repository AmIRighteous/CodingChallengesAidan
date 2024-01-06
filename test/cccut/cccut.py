import pytest
from src.cccut.cccut import parse_cli


@pytest.mark.parametrize("sys_argv, expected_result", [
    (["cccut.py", "-f2", "test.tsv"], {"columns": [2], "delimiter": "\t", "file_name": "test.tsv"}),
    (["cccut.py", "-f1", "-d,", "test.tsv"], {"columns": [1], "delimiter": ",", "file_name": "test.tsv"}),
    (["cccut.py", "-d,", "-f2", "fourchords.csv"], {"columns": [2], "delimiter": ",", "file_name": "fourchords.csv"}),
    (["cccut.py", "-f1,2", "sample.tsv"], {"columns": [1,2], "delimiter": "\t", "file_name": "sample.tsv"}),
    (["cccut.py", "-f\"1 2\"", "sample.tsv"], {"columns": [1,2], "delimiter": "\t", "file_name": "sample.tsv"}),
    (["cccut.py", "-f1", "-"], {"columns": [1], "delimiter": "\t", "stdin": True}),
    (["cccut.py", "-f1"], {"columns": [1], "delimiter": "\t", "stdin": True}),
])
def test_parse_cli(sys_argv, expected_result):
    flags = parse_cli(sys_argv)
    assert flags == expected_result

