# src/player.py
import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5  # Adjust speed as needed
        self.width = 40
        self.height = 40
        # Create a rect for collision detection and drawing
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction_vector):
        dx, dy = direction_vector
        if dx != 0 or dy != 0:
            # Normalize diagonal movement so diagonal isn't faster
            length = math.hypot(dx, dy)
            dx, dy = dx / length, dy / length
        
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        # Draw the player as a blue square
        pygame.draw.rect(surface, (0, 0, 255), self.rect)