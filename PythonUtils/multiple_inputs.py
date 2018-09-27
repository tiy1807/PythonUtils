# ------------------------------------------------------------------------------
# Class MultipleInput
#
# Allows the stacking of UserInputs. Often useful for multiple text inputs.
# ------------------------------------------------------------------------------

from PythonUtils.user_input import UserInput

class MultipleInput:
    def __init__(self, inputs, callback):
        # inputs should be a list of UserInput objects. Each will get called
        # in turn, and then the callback function wil be called with each
        # answer as an argument.
        self.inputs = inputs
        self.callback = callback

    def request_inputs(self):
        answers = []
        for input in self.inputs:
            rc = input.request_input()
            if rc == UserInput.ABORTED:
                break
            answers.append(input.get_answer())
        if rc != UserInput.ABORTED:
            self.callback(*answers)
