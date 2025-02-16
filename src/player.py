# src/player.py

import pygame

class Player:
    def __init__(self, x, y):
        # Load the knight image
        self.image = pygame.image.load("assets/knight.png").convert_alpha()
        # Optionally, scale the image to a desired size (for example, 50x50)
        self.image = pygame.transform.scale(self.image, (55, 50))
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 5

    def move(self, direction_vector):
        dx, dy = direction_vector
        # Normalize diagonal movement
        if dx != 0 or dy != 0:
            length = (dx**2 + dy**2) ** 0.5
            dx /= length
            dy /= length
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        # Draw the knight image at the player's position
        surface.blit(self.image, (self.x, self.y))