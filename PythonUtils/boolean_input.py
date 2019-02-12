# ------------------------------------------------------------------------------
# Class BooleanInput
#
# Allows the user to choose yes or no.
# ------------------------------------------------------------------------------

from PythonUtils.user_input import UserInput
from PythonUtils.option import Option

class BooleanInput(OptionInput):
    def __init__(self, text, default=None):
        OptionInput.__init__(self, text, [Option("Yes","Y","Affirmative"), Option("No","N","Negative")], default)
        pass

    def get_answer(self):
        return_value = False
        if self.chosen_option:
            if self.chosen_option.name == "Yes":
                return_value = True
            elif self.chosen_option.name == "No":
                return_value = False
            else:
                raise Exception(f"self.chosen_option.name should be Yes or No but was {self.chosen_option.name}")
        else:
            print("This question has not been asked. request_input has not been called, or has been with invalid input")
