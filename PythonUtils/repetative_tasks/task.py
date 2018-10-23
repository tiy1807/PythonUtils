# ------------------------------------------------------------------------------
# Class Task
#
# This object holds the relevant information relating to each task. As well as
# utility print functions.
# ------------------------------------------------------------------------------
import datetime

class Task:
    def __init__(self, name, frequency, last_completed=datetime.datetime.strftime(datetime.datetime.today(),"%d/%m/%Y")):
        # Units of frequency are in days
        self.frequency = datetime.timedelta(days=int(frequency))
        self.name = name
        self._last_complete = last_completed

    def last_completed_str(self):
        return self._last_complete

    def last_completed_datetime(self):
        return datetime.datetime.strptime(self._last_complete, "%d/%m/%Y")

    def due(self):
        return self.last_completed_datetime() + self.frequency

    def duration_left(self):
        return (self.due() - datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())).days

    def completed(self, time=datetime.datetime.strftime(datetime.datetime.today(),"%d/%m/%Y")):
        # Records into a file the completion hour of the task. Default is now.
        self._last_complete = time

    def to_string(self, max_name_length=0):
        return (self.name.ljust(max_name_length) + "\t-\t" + datetime.datetime.strftime(self.due(),"%d/%m/%y")
                + "\t-\t" + str(self.duration_left()))

    def to_csv(self):
        return [self.name, self.frequency.days, self.last_completed_str()]
