# src/level_manager.py

class LevelManager:
    def __init__(self):
        # Define level data as a list of dictionaries.
        # You can also load this from a JSON file later.
        self.levels = [
            {
                "player_start": (50, 50),
                "coins": [(150, 100), (300, 200), (500, 150)],
                "door": (700, 500),
                "time_limit": 30  # seconds
            },
            {
                "player_start": (50, 50),
                "coins": [(100, 300), (200, 400), (350, 250), (600, 100)],
                "door": (750, 450),
                "time_limit": 40  # seconds
            },
            # TODO: Add more levels as needed
        ]
        self.current_level_index = 0

    def get_current_level(self):
        return self.levels[self.current_level_index]

    def next_level(self):
        self.current_level_index += 1
        if self.current_level_index >= len(self.levels):
            # TODO: Handle win condition (e.g., show a win screen)
            self.current_level_index = 0  # For now, loop back to the first level