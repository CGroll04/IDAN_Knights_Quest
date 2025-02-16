# src/utils.py

class Timer:
    def __init__(self, time_limit):
        self.time_limit = time_limit
        self.current_time = time_limit

    def update(self, delta_time):
        self.current_time -= delta_time
        if self.current_time <= 0:
            self.current_time = 0
            return True  # Time's up
        return False

    def reset(self, time_limit=None):
        if time_limit is not None:
            self.time_limit = time_limit
        self.current_time = self.time_limit