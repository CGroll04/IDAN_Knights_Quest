# src/utils.py
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAIN_MARGIN = 50
MAIN_AREA = pygame.Rect(MAIN_MARGIN, MAIN_MARGIN,
                        SCREEN_WIDTH - 2 * MAIN_MARGIN,
                        SCREEN_HEIGHT - 2 * MAIN_MARGIN)

class Timer:
    def __init__(self, time_limit):
        self.time_limit = time_limit
        self.current_time = time_limit

    def update(self, delta_time):
        self.current_time -= delta_time
        if self.current_time <= 0:
            self.current_time = 0
            return True  # Time is up
        return False

    def reset(self, time_limit=None):
        if time_limit is not None:
            self.time_limit = time_limit
        self.current_time = self.time_limit