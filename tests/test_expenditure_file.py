import mock
import pytest
import json
import os
from PythonUtils.record_expenditure import ExpenditureFile
from PythonUtils.record_expenditure import ExpenditureRecord


@pytest.fixture(scope="module")
def file():
    expenditure_file = ExpenditureFile("tests/data/settings.json")
    yield expenditure_file


mock_inputs = {"When did you spend it?" : "01/01/2020",
               "How much have you spent?": "3.00",
               "Where did you spend it?": "Example Shop",
               "What type of expenditure was it?": "Food",
               "How many litres did you buy?": "12",
               "What is the mileage on the car?": "2000"}


def mock_input(prompt):
    possible_prompts = [short_prompt for short_prompt in mock_inputs.keys() if short_prompt in prompt]
    if len(possible_prompts) == 1:
        return mock_inputs[possible_prompts[0]]
    else:
        raise ValueError(f"{prompt} is not a recognised prompt")


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
        temp_settings = d / "settings.json"

        with open('tests/data/settings.json', "r") as master_settings:
            data = json.load(master_settings)
            data["files"]["expenditure"] = str(p)
        with open(temp_settings, "w") as test_settings:
            json.dump(data, test_settings)

        test_file = ExpenditureFile(temp_settings)
        with mock.patch('builtins.input', mock_input):
            test_file.add_record()

    def test_petrol(self, tmp_path):
        d = tmp_path / "expfiles"
        d.mkdir()
        p = d / "petrol_spending.csv"
        temp_settings = d / "settings.json"

        with open('tests/data/settings.json', "r") as master_settings:
            data = json.load(master_settings)
            data["files"]["petrol"] = str(p)
        with open(temp_settings, "w") as test_settings:
            json.dump(data, test_settings)

        with mock.patch('builtins.input', mock_input):
            expenditure_file = ExpenditureFile(temp_settings)
            expenditure_file.add_petrol_record()
            assert p.read_text() == "24/10/2020,2.00,12,2000\n"
