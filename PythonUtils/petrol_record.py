# ------------------------------------------------------------------------------
# Class PetrolRecord
#
# Contains detailed information about the purchase of petrol
# ------------------------------------------------------------------------------
import datetime
from PythonUtils.record import Record


class PetrolRecord(Record):
    def __init__(self, *args):
        super().__init__(*args)
        self.date = args[0]
        self.price = args[1]
        self.volume = args[2]
        self.mileage = args[3]

    def get_date(self):
        values = self.date.split("/")
        return datetime.date(int(values[2]), int(values[1]), int(values[0]))
