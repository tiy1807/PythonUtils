import datetime

class Results:
    def __init__(self, result_function, expiry_duration):
        self.result_function = result_function
        self.results = result_function()
        self.result_time = datetime.datetime.now()
        # expiry_duration is inputted in minutes and stored in seconds
        self.expiry_duration = expiry_duration*60

    def get_new_results(self):
        self.results = self.result_function()
        self.result_time = datetime.datetime.now()

    def show(self):
        current_time = datetime.datetime.now()
        result_age = current_time - self.result_time
        if result_age.seconds > self.expiry_duration:
            self.get_new_results()
        print(self.results)
        print("\nResults from " + self.result_time.strftime("%H:%M %d/%m/%Y"))
        print("#############################################################")
