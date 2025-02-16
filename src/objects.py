# src/objects.py
import pygame  # We'll use pygame's Rect for simple collision checks

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.radius = 10  # Used for drawing and collision detection

    def collect(self):
        self.collected = True

    def check_collision(self, player):
        # Create a circle for the coin and a rect for the player
        coin_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        player_rect = pygame.Rect(player.x, player.y, 40, 40)  # Same size as drawn in main.py
        return coin_rect.colliderect(player_rect)


class Door:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_locked = True

    def unlock(self):
        self.is_locked = False

    def lock(self):
        self.is_locked = True

    def check_collision(self, player):
        door_rect = pygame.Rect(self.x, self.y, 50, 80)
        player_rect = pygame.Rect(player.x, player.y, 40, 40)
        return door_rect.colliderect(player_rect)