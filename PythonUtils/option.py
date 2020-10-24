# ------------------------------------------------------------------------------
# Class Option
#
# Options for the UserInput class
# ------------------------------------------------------------------------------

# This is the same as UserInput.SUCCESS is a bit of fudge - should have a
# constants file
SUCCESS = 0

class Option:
    def __init__(self, name, short_name, help_text, callback=None,
                 return_value=SUCCESS,
                 return_content=""
                 ):
        self.name = name
        self.short_name = short_name
        self.help_text = help_text
        self.return_value = return_value
        self.return_content = return_content
        self.callback = callback

    def help_string(self):
        return self.name + " (" + self.short_name + ") " + self.help_text

    def __eq__(self, other):
        if isinstance(other, str):
            result = ((self.name == other) or (self.short_name == other))
        else:
            raise NotImplemented()
        return result

    def to_csv(self):
        return [self.name, self.short_name, self.help_text]

    def run(self, *params):
        print("Running Option with name: " + self.name)
        if self.callback is not None:
            if len(params) == 0:
                self.callback()
            else:
                self.callback(*params)
