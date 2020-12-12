import mock
import pytest
from PythonUtils.record_expenditure import ExpenditureFile
from PythonUtils.record_expenditure import ExpenditureRecord


@pytest.fixture(scope="module")
def file():
    file = ExpenditureFile("tests/data/expenditure.csv", "tests/data/test_expenditure_config.csv")
    yield file


class TestFile:
    def test_creation(self, file):
        assert(file.records[0].to_string() == "15/09/2017,2.1,Bus,Transport")

    def test_print_last(self, file, capsys):
        file.print_last_record(2)
        captured = capsys.readouterr()
        assert(captured.out == "24/10/2020,2.00,Test,Socialising Food\n24/10/2020,2.00,Test,House\n")

    def test_add_record(self, tmp_path):
        d = tmp_path / "expfiles"
        d.mkdir()
        p = d / "test.csv"
        test_file = ExpenditureFile(p, "tests/data/test_expenditure_config.csv")
        test_file.add_created_record()
