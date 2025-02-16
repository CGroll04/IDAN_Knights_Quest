# src/obstacles.py

import pygame
import random
from utils import MAIN_AREA

class MovingObstacle:
    def __init__(self, x, y, width, height, vx, vy, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
        self.image = image

    def update(self, walls):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left < MAIN_AREA.left or self.rect.right > MAIN_AREA.right:
            self.vx = -self.vx
            self.rect.x += self.vx
        if self.rect.top < MAIN_AREA.top or self.rect.bottom > MAIN_AREA.bottom:
            self.vy = -self.vy
            self.rect.y += self.vy

        for wall in walls:
            if self.rect.colliderect(wall):
                self.vx = -self.vx
                self.vy = -self.vy
                self.rect.x += self.vx
                self.rect.y += self.vy
                break

    def draw(self, surface):
        scaled_spider = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        surface.blit(scaled_spider, (self.rect.x, self.rect.y))

def create_obstacles(walls, obstacle_image, safe_rect, count=3, obs_width=30, obs_height=30):
    obstacles = []
    possible_speeds = [-4, -3, -2, 2, 3, 4]
    for _ in range(count):
        attempts = 0
        while attempts < 100:
            x = random.randint(MAIN_AREA.left, MAIN_AREA.right - obs_width)
            y = random.randint(MAIN_AREA.top, MAIN_AREA.bottom - obs_height)
            obs_rect = pygame.Rect(x, y, obs_width, obs_height)
            if not any(obs_rect.colliderect(wall) for wall in walls) and not obs_rect.colliderect(safe_rect):
                vx = random.choice(possible_speeds)
                vy = random.choice(possible_speeds)
                obstacles.append(MovingObstacle(x, y, obs_width, obs_height, vx, vy, obstacle_image))
                break
            attempts += 1
        if attempts >= 100:
            print("Failed to place an obstacle without collision; skipping one.")
    return obstacles