# src/level_manager.py

class LevelManager:
    def __init__(self):
        # Each level is a dictionary with:
        # - "player_start": (x, y)
        # - "coins": list of (x, y) positions
        # - "door": (x, y)
        # - "time_limit": int
        # - "walls": list of (x, y, width, height)
        self.levels = [
            # Level 1: A simple open area
            {
                "player_start": (50, 50),
                "coins": [(150, 100), (300, 200), (500, 150)],
                "door": (700, 500),
                "time_limit": 30,
                "walls": [
                    (100, 100, 200, 20),   # horizontal wall
                    (400, 300, 20, 200)    # vertical wall
                ]
            },
            # Level 2: A semi-maze layout
            {
                "player_start": (50, 300),
                "coins": [(120, 250), (350, 100), (600, 300), (400, 400)],
                "door": (750, 50),
                "time_limit": 40,
                "walls": [
                    (200, 200, 400, 20),   # long horizontal wall
                    (200, 200, 20, 200),   # left vertical block
                    (580, 200, 20, 200)    # right vertical block
                ]
            },
            # Level 3: Vertical walls forming corridors
            {
                "player_start": (50, 300),
                "coins": [
                    (150, 250), (150, 350),  # coins in the left corridor
                    (350, 250), (350, 350)   # coins in the right corridor
                ],
                "door": (700, 300),
                "time_limit": 50,
                "walls": [
                    (250, 200, 20, 200),  # vertical wall
                    (450, 200, 20, 200)   # another vertical wall
                ]
            },
            # Level 4: A central split wall; door y-coordinate adjusted to 520
            {
                "player_start": (400, 50),
                "coins": [(320, 150), (480, 150), (320, 350), (480, 350)],
                "door": (400, 520),  # Changed from (400,550) to (400,520) so the door fits
                "time_limit": 60,
                "walls": [
                    (200, 300, 150, 20),  # left segment
                    (400, 300, 200, 20)   # right segment
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