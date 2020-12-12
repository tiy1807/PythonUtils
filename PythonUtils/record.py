
class Record:
    def __init__(self, *args):
        self.value_tuple = args

    def to_csv(self):
        return self.value_tuple
