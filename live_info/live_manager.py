# ------------------------------------------------------------------------------
# This class manages the various services to provide a framework to display
# useful information to the user in rotation.
# ------------------------------------------------------------------------------
from live_info.live_speed import InternetInfo
from live_info.live_traffic import TrafficInfo
from live_info.live_rail import RailInfo
from live_info.live_email import EmailInfo
import datetime
from live_info.results import Results
from threading import Lock
from run_till_abort import WaitingForInput
import time

class Display:
    def __init__(self, item_list):
        self.item_list = item_list

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
            print("***************************************************************")
            print(datetime.datetime.now().strftime("%H:%M %d/%m/%Y"))
            for result in results:
                result.show()

            time.sleep(wait_time)

        lock.release()
