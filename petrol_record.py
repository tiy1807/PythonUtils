# ------------------------------------------------------------------------------
# Class PetrolRecord
#
# Contains detailed information about the purchase of petrol
# ------------------------------------------------------------------------------

class PetrolRecord:
    def __init__(self, date, price, volume, mileage):
        self.date = date
        self.price = price
        self.volume = volume
        self.mileage = mileage

    def to_csv(self):
        return [self.date, self.price, self.volume, self.mileage]
