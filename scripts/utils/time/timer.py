from threading import Timer as ThreadTimer
import time

class Timer:
    def __init__(self, time_in_sec):
        self.time_in_sec = time_in_sec
        self.start_time = None
        self.done = False
        self.event_listeners = []
        self.destroyed = False

    def destroy(self):
        self.destroyed = True

    def set_time(self, time_in_sec):
        self.time_in_sec = time_in_sec

    def set_done(self):
        self.done = True

    def start(self):
        self.done = False
        self.start_time = time.time()
        self.start_even_timer()

    def add_event_listener(self, function):
        self.event_listeners.append(function)

    def create_thread_timer(self, time, time_out_func):
        timer = ThreadTimer(time, time_out_func)
        timer.start()

    def start_even_timer(self):
        if len(self.event_listeners) != 0:
            self.create_thread_timer(self.time_in_sec, self.time_out)

    def time_out(self):
        if self.destroyed:
            return

        self.done = True

        for event_listener_function in self.event_listeners:
            event_listener_function()
            self.event_listeners.remove(event_listener_function)

    def get_time_left_in_seconds(self):
        time_from_start = time.time() - self.start_time
        time_left = self.time_in_sec - time_from_start

        if time_left < 0:
            return 0

        return time_left

    def is_time_passed(self):
        if self.done: return True

        time_from_start = time.time() - self.start_time
        # check that enought time is bassed from preparing
        if time_from_start >= self.time_in_sec:
            self.done = True
            return True

        return False
