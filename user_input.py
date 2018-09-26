# ------------------------------------------------------------------------------
# Text Command Line Interface
#
# This is a utility class which enables use of the command line for textual
# input by a user.
#
# It allows validity checking of the input, and loops until a correct input is
# recieved, with an escape sequence.
# ------------------------------------------------------------------------------
from option import Option
# ------------------------------------------------------------------------------
# Class UserInput
# This class is abstract and so these objects should not be created. The following
# functions must be included in any derived classes:
#  - _help_action
#  - _ask
#  - get_answer
#
# text    - a string. For nice formatting, don't end with a new line character
# default - the default value if the input is empty
#
# The API is as follows:
#  - The object must in instantiated
#  - .request_input() must be called. This returns an integer indicating whether the
#    operation was successful.
# ------------------------------------------------------------------------------
class UserInput:
    # Return codes for request_input
    NOT_SET = -1
    SUCCESS = 0
    ABORTED = 1
    HELP = 2
    INVALID_INPUT = 3

    def __init__(self, text, default=None):
        self.text = text
        self.default = default
        self.abort_message = "Input aborted"

        abort_opt = Option("\\abort","\\a","Aborts the current input",None,self.ABORTED)
        help_opt = Option("\\help","\\h","Prints help text for options",self.help_action,self.HELP)
        self.master_options = [abort_opt, help_opt]

    def help_action(self):
        help_string = "Priority Options\n"
        for option in self.master_options:
            help_string += option.help_string() + "\n"

        help_string += "\nInput Specific Help\n"
        help_string += self._help_action()
        print(help_string)

    def request_input(self):
        return_value = self.NOT_SET
        while return_value != self.SUCCESS and return_value != self.ABORTED:
            return_value = self._ask()

        if return_value == self.ABORTED:
            print(self.abort_message)

        return return_value

    def _help_action(self):
        # Returns a string to be appended to the help text.
        raise NotImplemented()

    def _ask(self):
        # In derived classes asks the user to make an input. Returns a return code
        # as codified above.
        raise NotImplemented()

    def get_answer(self):
        raise NotImplemented()
