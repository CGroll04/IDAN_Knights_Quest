# src/player.py

import pygame

class Player:
    def __init__(self, x, y):
        # Load the knight image
        self.image = pygame.image.load("assets/knight.png").convert_alpha()
        # Optionally, scale the image to a desired size (for example, 50x50)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.x = x
        self.y = y
        
        # Use the full image dimensions for drawing
        self.draw_width = self.image.get_width()
        self.draw_height = self.image.get_height()
        
        # Define the hitbox dimensions:
        # Let's say we want the hitbox to be 60% as wide as the image but keep the full height.
        hitbox_width = int(self.draw_width * 0.5)
        hitbox_height = self.draw_height
        
        # Create the hitbox rect and center it horizontally within the image.
        # We'll set the rect's top to be the same as the image's top.
        self.rect = pygame.Rect(self.x, self.y, hitbox_width, hitbox_height)
        # Center the hitbox relative to the image horizontally:
        self.rect.centerx = self.x + self.draw_width // 2
        
        self.speed = 5

    def move(self, direction_vector):
        dx, dy = direction_vector
        if dx != 0 or dy != 0:
            length = (dx**2 + dy**2) ** 0.5
            dx /= length
            dy /= length
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Update hitbox position (re-center it relative to the image position)
        self.rect.topleft = (self.x, self.y)
        self.rect.centerx = self.x + self.draw_width // 2

    def draw(self, surface):
        # Draw the knight image at the player's drawing position.
        surface.blit(self.image, (self.x, self.y))