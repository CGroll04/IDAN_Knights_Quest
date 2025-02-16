# src/level_manager.py

class LevelManager:
    def __init__(self):
        # Each level is a dictionary with:
        # - "player_start": (x, y)
        # - "coins": list of (x, y) positions
        # - "door": (x, y)
        # - "time_limit": int (in seconds)
        # - "walls": list of (x, y, width, height)
        #
        # All coordinates should be inside the main area.
        self.levels = [
            # Level 1: A simple open area (longer time)
            {
                "player_start": (100, 100),
                "coins": [(150, 150), (300, 200), (500, 150)],
                "door": (700, 500),
                "time_limit": 20,  # Longer time for the first level
                "walls": [
                    (100, 80, 200, 20),
                    (400, 300, 20, 150)
                ]
            },
            # Level 2: A semi-maze layout
            {
                "player_start": (100, 350),
                "coins": [(120, 320), (350, 150), (600, 350), (400, 400)],
                "door": (700, 100),
                "time_limit": 30,
                "walls": [
                    (200, 250, 400, 20),
                    (200, 250, 20, 150),
                    (580, 250, 20, 150)
                ]
            },
            # Level 3: Vertical walls forming corridors
            {
                "player_start": (100, 350),
                "coins": [
                    (150, 320), (150, 380),
                    (350, 320), (350, 380)
                ],
                "door": (700, 350),
                "time_limit": 30,
                "walls": [
                    (250, 300, 20, 150),
                    (450, 300, 20, 150)
                ]
            },
            # Level 4: A central split wall layout
            {
                "player_start": (400, 100),
                "coins": [(320, 150), (480, 150), (320, 350), (480, 350)],
                "door": (400, 520),
                "time_limit": 30,
                "walls": [
                    (200, 300, 150, 20),
                    (400, 300, 200, 20)
                ]
            }
        ]
        self.current_level_index = 0

    def get_current_level(self):
        return self.levels[self.current_level_index]

    def next_level(self):
        self.current_level_index += 1

    def reset(self):
        self.current_level_index = 0