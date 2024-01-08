import pytest
from src.cccut.cccut import parse_cli, read_file


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


# @pytest.mark.parametrize("sys_argv, expected_error", [
#     (["cccut.py", "-fa", "test.tsv"], '[]'),
#     (["cccut.py", "-f0", "test.tsv"], {}),
#     (["cccut.py", "-f\"1    2\"", "test.tsv"], {}),
#     (["cccut.py", "-f-1", "test.tsv"], {}),
#     (["cccut.py", "-f1", "-d", "test.tsv"], {}),
#     (["cccut.py", "-f1,a", "test.tsv"], {}),
# ])
# def test_parse_cli_fail(sys_argv, expected_error):
#     # add testing of parsing CLI where someone gives negative number, or invalid value for columns
#     try:
#         flags = parse_cli(sys_argv)
#     except RuntimeError as e:
#         assert e.args[0] == "ERROR: Unparsable flags, please revise these issues: "



@pytest.mark.parametrize("flags, expected_result", [
    ({"columns": [2], "delimiter": "\t","file_name": "test.tsv"}, [["f1"], ["1"]]),
    ({"columns": [2], "delimiter": ",","file_name": "test.csv"}, [["f1"], ["1"]]),
    ({"columns": [6], "delimiter": ",","file_name": "test.csv"}, []),
    ({"columns": [1,2,3,4,5], "delimiter": "\t","file_name": "test.tsv"}, [["f0","f1","f2","f3","f4"], ["0", "1", "2", "3", "4"]]),
    ({"columns": [1,2,3,4,5], "delimiter": ",","file_name": "test.csv"}, [["f0","f1","f2","f3","f4"], ["0", "1", "2", "3", "4"]]),
])
def test_file_parser(flags, expected_result):
    assert read_file(flags) == expected_result