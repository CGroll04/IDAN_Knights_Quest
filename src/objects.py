# src/objects.py
import pygame

class Coin:
    def __init__(self, x, y, width=20, height=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collected = False

    def collect(self):
        self.collected = True

    def check_collision(self, player):
        # Create a rect for the coin and check collision with the player's rect
        coin_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return coin_rect.colliderect(player.rect)

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
        # Define door dimensions (50x80 as before)
        door_rect = pygame.Rect(self.x, self.y, 50, 80)
        return door_rect.colliderect(player.rect)