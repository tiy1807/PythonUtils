from PythonUtils.live_info.results import Results

class DisplayItem:
    def __init__(self, expiry_duration):
        self.expiry_duration = expiry_duration

    def get_results(self):
        return Results(self.get_info, self.expiry_duration)

    def get_info(self):
        raise NotImplemented("Must define get_info function for this class")
