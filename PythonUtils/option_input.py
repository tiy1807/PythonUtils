# ------------------------------------------------------------------------------
# Class OptionInput
#
# Extends user input to mandate that a particular option be picked
# ------------------------------------------------------------------------------

from user_input import UserInput
import copy
import logging
from option import Option

class OptionInput(UserInput):
    def __init__(self, text, options, default=None):
        UserInput.__init__(self, text, default)
        self.logger = logging.getLogger('OptionInput')
        self.options = options
        self.chosen_option = None

        if self.default is not None:
            default_opt = None
            for option in options:
                if option == default:
                    self.logger.info("Setting default to:" + default)
                    self.default_opt = Option(option.name, "", "DEFAULT OPTION: " + option.help_text, option.callback)
                    self.master_options.append(self.default_opt)

    def _help_action(self):
        help_string = ""
        for option in self.options:
            help_string += option.help_string() + "\n"
        return help_string

    def get_answer(self):
        return self.chosen_option.name

    def _ask(self):
        if self.default is None:
            user_input = input(self.text + "\n")
        else:
            user_input = input(self.text + " (default: " + self.default_opt.name + ")\n")

        return_value = self.NOT_SET

        for option in self.master_options:
            if option == user_input:
                return_value = option.return_value
                self.chosen_option = option
                option.run()

        if return_value == self.NOT_SET:
            for option in self.options:
                if option == user_input:
                    return_value = self.SUCCESS
                    self.chosen_option = option
                    option.run()

        if return_value == self.NOT_SET:
            return_value = self.INVALID_INPUT
            print("Invalid input. Please try again. Type \\h for help.")

        return return_value
