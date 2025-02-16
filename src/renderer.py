# src/renderer.py

import pygame
import random
from utils import MAIN_AREA
from objects import Coin

def render_game(screen, bg_image, vert_wall_tex, horiz_wall_tex,
                door_closed_img, door_open_img, coin_img,
                player, coins, door, timer, walls, obstacles):
    screen.blit(bg_image, (0, 0))
    
    for wall in walls:
        texture = vert_wall_tex if wall.width < wall.height else horiz_wall_tex
        scaled_wall = pygame.transform.scale(texture, (wall.width, wall.height))
        screen.blit(scaled_wall, (wall.x, wall.y))
    
    for coin in coins:
        if not coin.collected:
            scaled_coin = pygame.transform.scale(coin_img, (coin.width, coin.height))
            screen.blit(scaled_coin, (coin.x, coin.y))
    
    door_image = door_open_img if not door.is_locked else door_closed_img
    scaled_door = pygame.transform.scale(door_image, (50, 80))
    screen.blit(scaled_door, (door.x, door.y))
    
    for obstacle in obstacles:
        obstacle.draw(screen)
    
    player.draw(screen)
    
    font = pygame.font.SysFont(None, 36)
    timer_text = font.render(f"Time: {int(timer.current_time)}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))
    
    pygame.display.flip()

def render_win_screen(screen, bg_image, total_time, restart_button_rect):
    screen.blit(bg_image, (0, 0))
    font = pygame.font.SysFont(None, 48)
    win_text = font.render("You Win!", True, (255, 255, 255))
    time_text = font.render(f"Total Time: {int(total_time)} seconds", True, (255, 255, 255))
    
    win_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    time_rect = time_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(win_text, win_rect)
    screen.blit(time_text, time_rect)
    
    pygame.draw.rect(screen, (0, 0, 255), restart_button_rect)
    button_font = pygame.font.SysFont(None, 36)
    button_text = button_font.render("Restart", True, (255, 255, 255))
    btn_text_rect = button_text.get_rect(center=restart_button_rect.center)
    screen.blit(button_text, btn_text_rect)
    
    pygame.display.flip()

def render_gameover_screen(screen, bg_image, levels_passed, restart_button_rect, gameover_reason):
    screen.blit(bg_image, (0, 0))
    font = pygame.font.SysFont(None, 48)
    over_text = font.render(gameover_reason, True, (255, 0, 0))
    levels_text = font.render(f"Levels Passed: {levels_passed}", True, (255, 255, 255))
    
    over_rect = over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    levels_rect = levels_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(over_text, over_rect)
    screen.blit(levels_text, levels_rect)
    
    pygame.draw.rect(screen, (0, 0, 255), restart_button_rect)
    button_font = pygame.font.SysFont(None, 36)
    button_text = button_font.render("Restart", True, (255, 255, 255))
    btn_text_rect = button_text.get_rect(center=restart_button_rect.center)
    screen.blit(button_text, btn_text_rect)
    
    pygame.display.flip()

def create_coins_in_area(coin_positions, walls, coin_width=20, coin_height=20):
    """Creates coins ensuring they are within MAIN_AREA."""
    coins = []
    for pos in coin_positions:
        x, y = pos
        x = max(MAIN_AREA.left, min(x, MAIN_AREA.right - coin_width))
        y = max(MAIN_AREA.top, min(y, MAIN_AREA.bottom - coin_height))
        coin_rect = pygame.Rect(x, y, coin_width, coin_height)
        collision = any(coin_rect.colliderect(wall) for wall in walls)
        attempts = 0
        while collision and attempts < 100:
            x = random.randint(MAIN_AREA.left, MAIN_AREA.right - coin_width)
            y = random.randint(MAIN_AREA.top, MAIN_AREA.bottom - coin_height)
            coin_rect = pygame.Rect(x, y, coin_width, coin_height)
            collision = any(coin_rect.colliderect(wall) for wall in walls)
            attempts += 1
        if collision:
            print(f"Skipping coin at {pos} after {attempts} attempts.")
            continue
        coins.append(Coin(x, y, coin_width, coin_height))
    return coins