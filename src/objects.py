# src/objects.py

import pygame

class Bullet:
    fireball_image = None  # Class variable for lazy loading

    @classmethod
    def load_image(cls):
        if cls.fireball_image is None:
            try:
                cls.fireball_image = pygame.image.load("assets/fireball.png").convert_alpha()
                print("Fireball image loaded with size:", cls.fireball_image.get_size())
            except Exception as e:
                print("Error loading fireball image:", e)
        return cls.fireball_image

    def __init__(self, x, y, direction, speed=10):
        self.x = x
        self.y = y
        self.direction = direction  # Should be normalized (dx, dy)
        self.speed = speed
        # Increase bullet size for visibility:
        self.width = 30
        self.height = 30
        self.radius = self.width // 2
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        Bullet.load_image()  # Ensure the image is loaded after pygame is initialized

    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
    # Comment out the image drawing for now:
        scaled_image = pygame.transform.scale(Bullet.fireball_image, (self.width, self.height))
        surface.blit(scaled_image, (self.rect.x, self.rect.y))

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
    