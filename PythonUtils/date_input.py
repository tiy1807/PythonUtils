from PythonUtils.text_input import TextInput

class DateInput(TextInput):
    def __init__(self, **kwargs):
        kwargs["regex"] = "[0-3][0-9]\/[0-1][0-9]\/20[1-3][0-9]"
        TextInput.__init__(self, **kwargs)