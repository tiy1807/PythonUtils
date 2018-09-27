import speedtest
import datetime
from PythonUtils.run_till_abort import WaitingForInput
from threading import Lock
from threading import Semaphore
import time
from PythonUtils.live_info.display_item import DisplayItem

class InternetInfo(DisplayItem):
    def __init__(self, expiry_duration):
        DisplayItem.__init__(self, expiry_duration)
        self.server = speedtest.Speedtest(timeout=300)
        self.server.get_servers()
        self.server.get_best_server()
        self.file_path = "results.txt"

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
        file_handler = open(self.file_path,'a')
        lock = Lock()

        # Creates a thread waiting for user input, which takes control of the
        # lock. lock is released when user input is detected
        wait_for_input = WaitingForInput(lock, "Press enter to stop recording " +
            "internet bandwidth")
        wait_for_input.start()
        wait_for_input.wait_till_up()

        while not lock.acquire(blocking=False):
            self.server.get_servers()
            self.server.get_best_server()
            self.test()
            file_handler.write(self.results_string() + "\n")
            time.sleep(interval)

        lock.release()
        file_handler.close()


if __name__ == "__main__":
    internet = InternetInfo()
    internet.record_speed(10)
