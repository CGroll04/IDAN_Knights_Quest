# src/input_handler.py
import pygame

def get_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        return "up"
    elif keys[pygame.K_DOWN]:
        return "down"
    elif keys[pygame.K_LEFT]:
        return "left"
    elif keys[pygame.K_RIGHT]:
        return "right"
    return None

# TODO: In the future, add functions here to integrate gyroscope/button inputs.