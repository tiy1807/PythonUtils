import speedtest
import datetime
from PythonUtils.run_till_abort import WaitingForInput
from threading import Lock
import time
from PythonUtils.live_info.display_item import DisplayItem
from PythonUtils.record import Record
from PythonUtils.storer import Store


class InternetInfo(DisplayItem):
    def __init__(self, expiry_duration):
        DisplayItem.__init__(self, expiry_duration)
        self.server = speedtest.Speedtest(timeout=300)
        self.server.get_servers()
        self.server.get_best_server()
        self.information_store = Store("internet_connectivity.csv", Record)

    def set_file(self, file_path):
        self.file_path = file_path

    def download_speed(self):
        return self.server.download()

    def test(self):
        self.server.download()
        self.server.upload()

    def results_string(self):
        results_dict = self.server.results.dict()
        return (datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " +
                "Ping " + str(results_dict['ping']) + " | " +
                "Download " + str(results_dict['download']) + " | " +
                "Upload " + str(results_dict['upload']))

    def get_info(self):
        self.test()
        return self.results_string()

    def record_speed(self, interval):
        # The interval between records is not accurate. Uses sleep, and thread
        # control but should be okay. interval is in seconds.
        lock = Lock()

        # Creates a thread waiting for user input, which takes control of the
        # lock. lock is released when user input is detected
        wait_for_input = WaitingForInput(lock, "Press enter to stop recording internet bandwidth")
        wait_for_input.start()
        wait_for_input.wait_till_up()

        while not lock.acquire(blocking=False):
            self.server.get_servers()
            self.server.get_best_server()
            self.test()
            results_dict = self.server.results.dict()
            is_connected = (results_dict['download'] > 0)
            self.information_store.write_new_record([datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                                     is_connected,
                                                     results_dict['ping'],
                                                     results_dict['download'],
                                                     results_dict['upload']])
            time.sleep(interval)

        lock.release()
