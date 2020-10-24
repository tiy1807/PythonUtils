# ------------------------------------------------------------------------------
# Class ListInput
#
# Allows the same Input object to be requested multiple times, either a
# predefined number of times or until the user enters the 'finished' sequence.
# ------------------------------------------------------------------------------

from PythonUtils.option import Option
from PythonUtils.user_input import UserInput

class ListInput:
    REPEAT_TILL_TERMINATED = 0
    REPEAT_FINITELY = 1

    def __init__(self, input, repeats):
        self.input = input
        finished_opt = Option(name="\\finished", short_name="\\f", help_text="Stops asking this question")
        self.input.master_options.append(finished_opt)
        self.input.default_opt = finished_opt
        self.input.default = finished_opt.short_name

        self.repeats = repeats
        if self.repeats == self.REPEAT_TILL_TERMINATED:
            self.termination = self.REPEAT_TILL_TERMINATED
        elif self.repeats > 0:
            self.termination = self.REPEAT_FINITELY
        self.answer = []

    def get_answer(self):
        return self.answer

    def request_input(self):
        ask_again = True
        number_of_asks = 0

        while ask_again:
            rc = self.input.request_input()
            answer = self.input.get_answer()

            if rc == UserInput.SUCCESS:
                if self.termination == self.REPEAT_FINITELY:
                    ask_again = (number_of_asks < self.repeats)
                elif self.termination == self.REPEAT_TILL_TERMINATED:
                    ask_again = (answer != "\\finished")
                else:
                    raise ValueError()
            else:
                ask_again = (rc != UserInput.ABORTED)

            if (answer != "\\finished"):
                self.answer.append(self.input.get_answer())
                number_of_asks += 1

        return rc
