# ------------------------------------------------------------------------------
# Class TextInput
#
# Allows the user to input text (as opposed to predefined options)
# ------------------------------------------------------------------------------

from user_input import UserInput
from option import Option

class TextInput(UserInput):
    def __init__(self, text, default=None):
        UserInput.__init__(self, text, default)
        self.help_string = "No input check is made, any is valid"
        if default:
            self.help_string += "\nThe default value is: " + str(default)

    def _help_action(self):
        return self.help_string

    def get_answer(self):
        return self.answer

    def _ask(self):
        user_input = input(self.text)
        return_value = self.NOT_SET

        for option in self.master_options:
            if option == user_input:
                return_value = option.return_value
                option.run()

        if return_value == self.NOT_SET:
            return_value = self.SUCCESS
            if user_input == "":
                self.answer = self.default
            else:
                self.answer = user_input

        return return_value
