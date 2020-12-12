import mock
from PythonUtils.text_input import TextInput
from PythonUtils.user_input import UserInput


def test_input():
    with mock.patch('builtins.input', return_value="correct_value"):
        tui = TextInput("An example question")
        assert(tui.request_input() == UserInput.SUCCESS)
        assert(tui.get_answer() == "correct_value")


def test_help():
    with mock.patch('builtins.input', return_value="\\h"):
        tui = TextInput("An example question")
        assert(tui._ask() == UserInput.HELP)


def test_default():
    with mock.patch('builtins.input', return_value=""):
        tui = TextInput("An example question", "default answer")
        assert(tui.request_input() == UserInput.SUCCESS)
        assert(tui.get_answer() == "default answer")


def test_valid_regex():
    with mock.patch('builtins.input', return_value="54.23"):
        tui = TextInput(text="An example question", default="0.00", regex="[0-9]+\\.[0-9]{2}")
        assert(tui.request_input() == UserInput.SUCCESS)
        assert(tui.get_answer() == "54.23")


def test_invalid_regex():
    with mock.patch('builtins.input', return_value="invalid_text"):
        tui = TextInput(text="An example question", default="0.00", regex="[0-9]+\\.[0-9]{2}")
        assert(tui._ask() == UserInput.INVALID_INPUT)
