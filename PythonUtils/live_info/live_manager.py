# ------------------------------------------------------------------------------
# This class manages the various services to provide a framework to display
# useful information to the user in rotation.
# ------------------------------------------------------------------------------
import datetime
from threading import Lock
from PythonUtils.run_till_abort import WaitingForInput
import time

class Display:
    def __init__(self, item_list):
        self.item_list = item_list
        self.restricted_time_activity = False

    def set_active_time(self, start, end):
        self.restricted_time_activity = True
        self.start_time = start
        self.end_time = end

    def show_display(self):
        results = [display_item.get_results() for display_item in self.item_list]

        # Expiry duration is in seconds so wait time has units seconds
        wait_time = min([result.expiry_duration for result in results])

        lock = Lock()
        # Creates a thread waiting for user input, which takes control of the
        # lock. lock is released when user input is detected.
        wait_for_input = WaitingForInput(lock, "")
        wait_for_input.start()
        wait_for_input.wait_till_up()

        while not lock.acquire(blocking=False):
            if self.restricted_time_activity:
                if ((datetime.datetime.now().time() > self.start_time) and
                    datetime.datetime.now().time() < self.end_time):
                    print("***************************************************************")
                    print(datetime.datetime.now().strftime("%H:%M %d/%m/%Y"))
                    for result in results:
                        result.show()
                    time.sleep(wait_time)
                else:
                    print(datetime.datetime.now().strftime("%H:%M %d/%m/%Y") + ": Not in active window, sleeping for an hour")
                    time.sleep(3600)
            else:
                print("***************************************************************")
                print(datetime.datetime.now().strftime("%H:%M %d/%m/%Y"))
                for result in results:
                    result.show()
                time.sleep(wait_time)

        lock.release()
