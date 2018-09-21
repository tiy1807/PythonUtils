# ------------------------------------------------------------------------------
# run_till_abort.py
#
# This file provides a class which enables a function to run in a loop until
# the user provides an input.
# ------------------------------------------------------------------------------

from threading import Thread
from user_input import UserInput

# ------------------------------------------------------------------------------
# class WaitingForInput
#
# This class must be initialised with a lock and a semaphore. The calling code
# must call wait_till_up to guarantee that the lock has been acquired.
# ------------------------------------------------------------------------------
from threading import Semaphore

class WaitingForInput(Thread):
    def __init__(self, lock, user_text, valid_options=[]):
        Thread.__init__(self)
        # Initialises a thread. Stores the callback function.
        self.lock = lock
        self.sem_ready = Semaphore(0)
        self.lock.acquire()
        self.user_input = UserInput(user_text, valid_options)

    def run(self):
        self.sem_ready.release()
        self.user_input.request_input()
        self.lock.release()

    def wait_till_up(self):
        self.sem_ready.acquire()
