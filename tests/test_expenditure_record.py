import mock
import pytest
from PythonUtils.option import Option
from PythonUtils.record_expenditure import ExpenditureRecord


@pytest.mark.parametrize("test_record, expected_output",
                         [
                             ("01/01/2020,3.00,Example Shop,Food",
                              {"date": "01/01/2020", "amount": "3.00", "where": "Example Shop", "type": "Food"}
                              ),
                             ("28/02/2019,100.00,Amazon,Presents",
                              {"date": "28/02/2019", "amount": "100.00", "where": "Amazon", "type": "Presents"}
                              )
                         ])
def test_read(test_record, expected_output):
    record = ExpenditureRecord(test_record, 'r')
    assert record.valid
    assert(record.date == expected_output["date"])
    assert(record.amount == expected_output["amount"])
    assert(record.where == expected_output["where"])
    assert(record.type == expected_output["type"])


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
        raise ValueError("{prompt} is not a recognised prompt")


class TypeContainerStub:
    def __init__(self):
        self.object_list = [Option("Food", "Food", "Food")]


def test_write():
    with mock.patch('builtins.input', mock_input):
        record = ExpenditureRecord(TypeContainerStub(), "w")
        assert record.valid
        assert (record.date == mock_inputs["When did you spend it?"])
        assert (record.amount == mock_inputs["How much have you spent?"])
        assert (record.where == mock_inputs["Where did you spend it?"])
        assert (record.type == mock_inputs["What type of expenditure was it?"])


def test_append(tmp_path):
    d = tmp_path / "expfiles"
    d.mkdir()
    p = d / "test.csv"
    record = ExpenditureRecord("01/01/2020,3.00,Example Shop,Food", 'r')
    record.append_to_file(p)
    assert p.read_text() == "01/01/2020,3.00,Example Shop,Food\n"


def test_string():
    record = ExpenditureRecord("01/01/2020,3.00,Example Shop,Food", 'r')
    assert record.to_string() == "01/01/2020,3.00,Example Shop,Food"
