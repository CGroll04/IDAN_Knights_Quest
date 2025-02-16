# src/main.py

import pygame
import random
from level_manager import LevelManager
from player import Player  # Player loads knight.png and has a custom hitbox.
from objects import Coin, Door, Bullet  # Make sure Bullet is defined in objects.py.
from obstacles import create_obstacles  # from obstacles.py, which defines MovingObstacle.
from input_handler_keyboard import get_input
from renderer import render_game, render_win_screen, render_gameover_screen, create_coins_in_area
from utils import Timer, MAIN_AREA, SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("IDAN Pong: Your New Adventure")
    clock = pygame.time.Clock()

    # Load and scale the background image to fill the window.
    original_bg = pygame.image.load("assets/background.png").convert()
    bg_image = pygame.transform.scale(original_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Load wall textures.
    vertical_wall_texture = pygame.image.load("assets/vertical_wall.png").convert()
    horizontal_wall_texture = pygame.image.load("assets/horizontal_wall.png").convert()
    
    # Load door images.
    door_closed_img = pygame.image.load("assets/door_closed.png").convert_alpha()
    door_open_img = pygame.image.load("assets/door_open.png").convert_alpha()
    
    # Load coin image.
    coin_img = pygame.image.load("assets/coin.png").convert_alpha()
    
    # Load spider image for obstacles.
    spider_img = pygame.image.load("assets/spider.png").convert_alpha()
    
    # Initialize game state.
    game_state = "playing"  # can be "playing", "win", "gameover"
    total_time = 0.0
    gameover_reason = ""
    
    # Initialize level manager and load current level.
    level_manager = LevelManager()
    current_level = level_manager.get_current_level()
    
    walls = [pygame.Rect(x, y, w, h) for (x, y, w, h) in current_level["walls"]]
    player = Player(*current_level["player_start"])
    coins = create_coins_in_area(current_level["coins"], walls)
    door = Door(*current_level["door"])
    timer = Timer(current_level["time_limit"])
    
    # Create a safe zone for obstacles around the player's spawn (100-pixel margin).
    safe_margin = 100
    safe_rect = pygame.Rect(
        player.x - safe_margin, player.y - safe_margin,
        player.draw_width + 2 * safe_margin, player.draw_height + 2 * safe_margin
    )
    
    obstacles = create_obstacles(walls, spider_img, safe_rect, count=3, obs_width=30, obs_height=30)
    
    # Initialize bullet list and last_direction variable.
    bullets = []
    last_direction = (0, -1)  # Default to upward if no movement.
    
    # Define restart button for win and gameover screens.
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 50, 120, 50)
    
    running = True
    while running:
        delta_time = clock.get_time() / 1000.0  # seconds.
        if game_state == "playing":
            total_time += delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Bullet creation: when space is pressed, fire a bullet.
            if game_state == "playing" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create bullet from center of the player using last_direction.
                    bullet_x = player.x + player.draw_width // 2
                    bullet_y = player.y + player.draw_height // 2
                    new_bullet = Bullet(bullet_x, bullet_y, last_direction, speed=10)
                    bullets.append(new_bullet)
            
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
                    bullets = []
                    total_time = 0.0
                    game_state = "playing"

        if game_state == "playing":
            # Get input from gyroscope (or keyboard fallback).
            direction_vector = get_input()
            if direction_vector != (0, 0):
                last_direction = direction_vector  # Update last known direction.
            
            # Save player's previous position (for sliding).
            prev_x, prev_y = player.x, player.y
            
            # Move horizontally.
            player.x += direction_vector[0] * player.speed
            player.rect.x = player.x + (player.draw_width - player.rect.width) // 2
            for wall in walls:
                if player.rect.colliderect(wall):
                    player.x = prev_x
                    player.rect.x = prev_x + (player.draw_width - player.rect.width) // 2
                    break
            
            # Move vertically.
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
            
            # Update bullets.
            for bullet in bullets[:]:
                bullet.update()
                # Remove bullet if outside MAIN_AREA.
                if (bullet.x < MAIN_AREA.left or bullet.x > MAIN_AREA.right or
                    bullet.y < MAIN_AREA.top or bullet.y > MAIN_AREA.bottom):
                    bullets.remove(bullet)
                else:
                    # Check collision with obstacles.
                    for obstacle in obstacles[:]:
                        if bullet.rect.colliderect(obstacle.rect):
                            obstacles.remove(obstacle)
                            if bullet in bullets:
                                bullets.remove(bullet)
                            break
            
            # Update obstacles and check collision with player.
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
            
            # Check if player reaches door.
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
                    bullets = []
            
            # Update timer; if time runs out, game over.
            if timer.update(delta_time):
                game_state = "gameover"
                gameover_reason = "Time Ran Out!"
            
            # Render the game scene.
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