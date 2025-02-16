# src/player.py

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5  # Adjust speed as needed

    def move(self, direction):
        if direction == "up":
            self.y -= self.speed
        elif direction == "down":
            self.y += self.speed
        elif direction == "left":
            self.x -= self.speed
        elif direction == "right":
            self.x += self.speed
        # TODO: Add boundary checks if you want to prevent leaving the room