import ibuddy_usbapi as usb
from optparse import OptionParser
import time
from threading import Thread
from threading import Lock
from threading import Semaphore
from Queue import Queue
import logging

logger = logging.getLogger(__name__)
logfile = "ibuddy_timer.log"

def secs_to_mins(secs):
    return secs/60.0

def mins_to_secs(mins):
    return mins*60

class WaitForInput(Thread):
    def __init__(self, sem_ready, snoozer):
        Thread.__init__(self)
        self.name = "waiting_for_input"
        self.sem = sem_ready
        self.snooze = snoozer
        logger.debug("Creating lock")
        self.lock = Lock()

    def run(self):
        logger.debug("Trying to lock")
        self.lock.acquire()
        # Signal thread is ready
        self.sem.release()
        logger.debug("Successfully locked. Waiting for acknowledgement.")

        success = False
        while not success:
            tui = raw_input("Please enter snooze duration (seconds)")
            try:
                snooze_duration = int(tui)
                success = True
            except:
                print("Please enter an integer")
                sucess = False

        if snooze_duration > 0:
            logger.debug("Adding snooze to queue")
            self.snooze.put(snooze_duration)

        logger.debug("Acknowledgement received. Releasing lock.")
        self.lock.release()
        return tui

    def is_locked(self):
        logger.debug("Starting is_locked. Is this lock locked?")
        if not self.lock.acquire(False):
            # If the mutex is already locked
            return_value = True
        else:
            # The mutex wasn't locked but we now have it so release
            return_value = False
            self.lock.release()
        logger.debug("%s", return_value)
        return return_value

class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.snoozer = Queue()
        # Stores the times of events for logging purposes.
        # initial_time is the time in seconds since epoch
        # Entries are tuples (,) one when acknowledgement was requested, the
        # second when acknowledgement is given.
        self.times = []

    def timer_time(self):
        return time.time() - self.start_time

    def sleep_interval(self, duration, require_ack):
        time.sleep(duration)
        logger.info("Waking from sleep")

        if require_ack:
            thread_start_up = Semaphore(0)
            wait_for_input = WaitForInput(thread_start_up, self.snoozer)
            logger.info("Starting wait for input thread")
            wait_for_input.start()
            thread_start_up.acquire()
            # Acknoweldgement requested
            ack_requested = self.timer_time()
            logger.debug("Acknowledgement requested at %s", ack_requested)
            while wait_for_input.is_locked():
                devices.play('rdf')
                devices.wait()
                if not devices:
                    # No devices present means no time delay between checking for
                    # user input. (Usually caused by devices.wait())
                    time.sleep(1)
        else:
            ack_requested = self.timer_time()
            logger.info("Playing alert which doesn't require acknoweldgement")
            devices.play('bdf')
            devices.wait()

        print("Acknowledgement delay (s)" + str((self.timer_time() - ack_requested)/60))
        self.times.append((ack_requested,self.timer_time()))

    def sleep(self, duration, nu_intervals, require_ack):
        for interval in range(0,nu_intervals):
            logger.info("Sleep number %s. Sleeping for %s",
                        interval+1, duration/nu_intervals)
            self.sleep_interval(mins_to_secs(duration/nu_intervals),
                                require_ack or (interval == (nu_intervals -1)))

            while not self.snoozer.empty():
                logger.debug("Removing snooze from queue")
                snooze_duration = self.snoozer.get()
                self.snooze(snooze_duration)

            logger.debug("Sleep number %s finished. Current time is %s",
                         interval+1,
                         self.times[-1][1])

        logger.info("Timer has finished. Sleep duration %s. Total duration %s.",
                    duration,
                    self.times[-1][1])

    def snooze(self, duration):
        logger.info("Snoozing for %s seconds", duration)
        self.sleep_interval(secs_to_mins(duration), True)
        logger.info("Snooze completed")

if __name__ == "__main__":

    logging.basicConfig(filename=logfile, level=logging.DEBUG, filemode="w",
                        format='%(relativeCreated)6d %(threadName)s %(message)s')

    parser = OptionParser()

    parser.add_option("-d", "--duration", type="float", dest="dur", help="The length of time "
                      "to be measured.", default=60)
    parser.add_option("-i", type="int", dest="nu_intervals", help="The number of "
                      "intervals to split the time into.", default=1)
    parser.add_option("-f", action="store_true", dest="require_ack",
                      help="If present every interval requires ack")
    parser.add_option("-l", choices=['DEBUG','INFO','ERROR'], dest="logging_level",
                      help="Determines the logging level",default='INFO')

    (options, args) = parser.parse_args()

    if options.logging_level == 'DEBUG':
        log_level = logging.DEBUG
    elif options.logging_level == 'INFO':
        log_level = logging.INFO
    elif options.logging_level == 'ERROR':
        log_level = logging.ERROR

    logger.setLevel(log_level)

    logger.debug("Running with:\n\t\tduration = %s seconds\n\t\t%s intervals\n\t\t"
                 "Keyboard acknowledgement is %s",
                 options.dur*60,
                 options.nu_intervals,
                 options.require_ack)

    logger.debug("Finding devices")
    devices = usb.usbapi().getDevices()
    logger.debug("Found %s devices", len(devices))

    if len(devices) == 0:
        logger.error("No devices present")

    timer = Timer()
    timer.sleep(options.dur,options.nu_intervals,options.require_ack)
