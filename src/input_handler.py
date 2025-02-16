# src/input_handler.py
import pygame

def get_input():
    """
    Returns a tuple (dx, dy) representing the movement direction.
    For example:
      - (0, -1) is up
      - (1, 0) is right
      - (-1, -1) is up-left diagonal
    If no keys are pressed, returns (0, 0).
    """
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0

    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1
    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1

    return (dx, dy)