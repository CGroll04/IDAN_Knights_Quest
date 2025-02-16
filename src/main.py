# src/main.py

import pygame
import random
from level_manager import LevelManager
from player import Player
from objects import Coin, Door
from obstacles import create_obstacles, MovingObstacle
from input_handler_keyboard import get_input
from renderer import render_game, render_gameover_screen, render_win_screen
from utils import Timer, MAIN_AREA

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the main playable area (invisible boundary) with a 50-pixel margin.
MAIN_MARGIN = 50
MAIN_AREA = pygame.Rect(MAIN_MARGIN, MAIN_MARGIN,
                        SCREEN_WIDTH - 2 * MAIN_MARGIN,
                        SCREEN_HEIGHT - 2 * MAIN_MARGIN)

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("IDAN Pong: Your New Adventure")
    clock = pygame.time.Clock()
    
    # Load and scale background
    original_bg = pygame.image.load("assets/background.png").convert()
    bg_image = pygame.transform.scale(original_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Load wall textures
    vertical_wall_texture = pygame.image.load("assets/vertical_wall.png").convert()
    horizontal_wall_texture = pygame.image.load("assets/horizontal_wall.png").convert()
    
    # Load door images
    door_closed_img = pygame.image.load("assets/door_closed.png").convert_alpha()
    door_open_img = pygame.image.load("assets/door_open.png").convert_alpha()
    
    # Load coin image
    coin_img = pygame.image.load("assets/coin.png").convert_alpha()
    
    # Load spider image for obstacles
    spider_img = pygame.image.load("assets/spider.png").convert_alpha()
    
    # Initialize game state variables.
    game_state = "playing"  # "playing", "win", "gameover"
    total_time = 0.0
    gameover_reason = ""
    
    # Initialize level manager and current level
    level_manager = LevelManager()
    current_level = level_manager.get_current_level()
    
    walls = [pygame.Rect(x, y, w, h) for (x, y, w, h) in current_level["walls"]]
    player = Player(*current_level["player_start"])
    coins = create_coins_in_area(current_level["coins"], walls)
    door = Door(*current_level["door"])
    timer = Timer(current_level["time_limit"])
    
    # Define a safe zone for obstacles around the player's spawn (100-pixel margin)
    safe_margin = 100
    safe_rect = pygame.Rect(
        player.x - safe_margin, player.y - safe_margin,
        player.draw_width + 2 * safe_margin, player.draw_height + 2 * safe_margin
    )
    
    obstacles = create_obstacles(walls, spider_img, safe_rect, count=3, obs_width=30, obs_height=30)
    
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 50, 120, 50)
    
    running = True
    while running:
        delta_time = clock.get_time() / 1000.0
        if game_state == "playing":
            total_time += delta_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state in ("win", "gameover") and event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    level_manager.reset()
                    current_level = level_manager.get_current_level()
                    walls = [pygame.Rect(x, y, w, h) for (x, y, w, h) in current_level["walls"]]
                    player.x, player.y = current_level["player_start"]
                    player.rect.topleft = (player.x, player.y)
                    coins = create_coins_in_area(current_level["coins"], walls)
                    door.x, door.y = current_level["door"]
                    door.lock()
                    timer.reset(current_level["time_limit"])
                    safe_rect = pygame.Rect(
                        player.x - safe_margin, player.y - safe_margin,
                        player.draw_width + 2 * safe_margin, player.draw_height + 2 * safe_margin
                    )
                    obstacles = create_obstacles(walls, spider_img, safe_rect, count=3, obs_width=30, obs_height=30)
                    total_time = 0.0
                    game_state = "playing"
        
        if game_state == "playing":
            # Get movement input from input_handler.
            direction_vector = get_input()
            # Save previous position.
            prev_x, prev_y = player.x, player.y
            
            # Apply horizontal movement first.
            player.x += direction_vector[0] * player.speed
            player.rect.x = player.x + (player.draw_width - player.rect.width) // 2
            for wall in walls:
                if player.rect.colliderect(wall):
                    player.x = prev_x
                    player.rect.x = prev_x + (player.draw_width - player.rect.width) // 2
                    break
            
            # Apply vertical movement.
            player.y += direction_vector[1] * player.speed
            player.rect.y = player.y
            for wall in walls:
                if player.rect.colliderect(wall):
                    player.y = prev_y
                    player.rect.y = prev_y
                    break
            
            # Enforce boundaries using MAIN_AREA.
            if player.x < MAIN_AREA.left:
                player.x = MAIN_AREA.left
            if player.x + player.draw_width > MAIN_AREA.right:
                player.x = MAIN_AREA.right - player.draw_width
            if player.y < MAIN_AREA.top:
                player.y = MAIN_AREA.top
            if player.y + player.draw_height > MAIN_AREA.bottom:
                player.y = MAIN_AREA.bottom - player.draw_height
            player.rect.topleft = (player.x, player.y)
            player.rect.x = player.x + (player.draw_width - player.rect.width) // 2
            
            # Update obstacles.
            for obstacle in obstacles:
                obstacle.update(walls)
                if player.rect.colliderect(obstacle.rect):
                    game_state = "gameover"
                    gameover_reason = "You Died!"
            
            # Check coin collisions.
            for coin in coins:
                if not coin.collected and coin.check_collision(player):
                    coin.collect()
            
            # Unlock door if all coins collected.
            if all(coin.collected for coin in coins):
                door.unlock()
            
            # Check door.
            if door.check_collision(player) and not door.is_locked:
                level_manager.next_level()
                if level_manager.current_level_index >= len(level_manager.levels):
                    game_state = "win"
                else:
                    current_level = level_manager.get_current_level()
                    walls = [pygame.Rect(x, y, w, h) for (x, y, w, h) in current_level["walls"]]
                    player.x, player.y = current_level["player_start"]
                    player.rect.topleft = (player.x, player.y)
                    coins = create_coins_in_area(current_level["coins"], walls)
                    door.x, door.y = current_level["door"]
                    door.lock()
                    timer.reset(current_level["time_limit"])
                    safe_rect = pygame.Rect(
                        player.x - safe_margin, player.y - safe_margin,
                        player.draw_width + 2 * safe_margin, player.draw_height + 2 * safe_margin
                    )
                    obstacles = create_obstacles(walls, spider_img, safe_rect, count=3, obs_width=30, obs_height=30)
            
            # Update timer; if time runs out, game over.
            if timer.update(delta_time):
                game_state = "gameover"
                gameover_reason = "Time Ran Out!"
            
            render_game(
                screen,
                bg_image,
                vertical_wall_texture,
                horizontal_wall_texture,
                door_closed_img,
                door_open_img,
                coin_img,
                player,
                coins,
                door,
                timer,
                walls,
                obstacles
            )
        
        elif game_state == "win":
            render_win_screen(screen, bg_image, total_time, restart_button)
        
        elif game_state == "gameover":
            render_gameover_screen(screen, bg_image, level_manager.current_level_index, restart_button, gameover_reason)
        
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()