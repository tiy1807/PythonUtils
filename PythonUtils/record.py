
class Record:
    def __init__(self, *args):
        self.value_tuple = args

    def __eq__(self, other):
        return self.value_tuple == other.value_tuple

    def to_csv(self):
        return self.value_tuple
