import mock
from PythonUtils.date_input import DateInput
from PythonUtils.user_input import UserInput


def test_default():
    with mock.patch('builtins.input', return_value=""):
        tui = DateInput(text="Input date", default="12/12/2020")
        assert(tui.request_input() == UserInput.SUCCESS)
        assert(tui.get_answer() == "12/12/2020")


def test_invalid_input():
    with mock.patch('builtins.input', return_value="31/31/2020"):
        tui = DateInput(text="Input date")
        assert(tui._ask() == UserInput.INVALID_INPUT)


def test_valid_input():
    with mock.patch('builtins.input', return_value="01/01/2020"):
        tui = DateInput(text="Input date")
        assert(tui.request_input() == UserInput.SUCCESS)
        assert(tui.get_answer() == "01/01/2020")