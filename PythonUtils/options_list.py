# ------------------------------------------------------------------------------
# Class OptionList
#
# Container for Options objects
# ------------------------------------------------------------------------------

from PythonUtils.option import Option
from PythonUtils.object_list import ObjectList
from PythonUtils.text_input import TextInput
from PythonUtils.multiple_inputs import MultipleInput

class OptionList(ObjectList):
    def __init__(self, option_list=[]):
        ObjectList.__init__(self, Option, option_list)

    def add_option(self):
        tui_name = TextInput("Name the new option:")
        tui_short_name = TextInput("Provide the short name:")
        tui_help_text = TextInput("Add help text")
        tui_ask = MultipleInput([tui_name,tui_short_name,tui_help_text],self._add)
        tui_ask.request_inputs()
