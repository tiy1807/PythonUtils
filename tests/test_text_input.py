import mock
from PythonUtils.text_input import TextInput
from Pythonutils.user_input import UserInput

def text_input():
    with mock.patch.object(__builtin__,'input', lambda: "correct_value"):
        tui = TextInput("An example question")
        assert(tui.request_input() == UserInput.SUCCESS)
        assert(tui.get_answer() == "correct_value")

def test_help():
    with mock.patch.object(__builtin__,'input', lambda: "\\h"):
        tui = TextInput("An example question")
        assert(tui._ask() == UserInput.HELP)

def test_default():
    with mock.patch.object(__builtin__,'input', lambda: ""):
        tui = TextInput("An example question","default answer")
        assert(tui.request_input() == UserInput.SUCCESS)
        assert(tui.get_answer() == "default answer")

