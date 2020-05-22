# ------------------------------------------------------------------------------
# Class TextInput
#
# Allows the user to input text (as opposed to predefined options)
# ------------------------------------------------------------------------------

from PythonUtils.user_input import UserInput
from PythonUtils.option import Option
import re

class TextInput(UserInput):
    def __init__(self, text, default=None, regex=None):
        UserInput.__init__(self, text, default)
        if regex:
            self.regex = re.compile(regex)
            self.help_string = "Input must conform to regex " + regex
        else:
            self.regex = None
            self.help_string = "No input check is made, any is valid"
        if default:
            self.help_string += "\nThe default value is: " + str(default)

    def _help_action(self):
        return self.help_string

    def get_answer(self):
        return self.answer

    def _ask(self):
        if self.default is None:
            user_input = input(self.text + "\n")
        else:
            user_input = input(self.text + " (default: " + self.default + ")\n")
        return_value = self.NOT_SET

        for option in self.master_options:
            if option == user_input:
                return_value = option.return_value
                option.run()

        if return_value == self.NOT_SET:
            if user_input == "":
                self.answer = self.default
                return_value = self.SUCCESS
            else:
                if self.regex:
                    if self.regex.fullmatch(user_input):
                        return_value = self.SUCCESS
                        self.answer = user_input
                    else:
                        return_value = self.INVALID_INPUT
                        print(self.help_string)
                else:
                    return_value = self.SUCCESS
                    self.answer = user_input

        return return_value
