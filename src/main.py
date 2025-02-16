# src/main.py

import pygame
import random
from level_manager import LevelManager
from player import Player
from objects import Coin, Door
from input_handler import get_input
from utils import Timer

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def render_game(screen, bg_image, vert_wall_tex, horiz_wall_tex, door_closed_img, door_open_img, player, coins, door, timer, walls):
    """
    Renders the scene.
      - bg_image: Scaled background image (800x600).
      - vert_wall_tex: Texture for vertical walls.
      - horiz_wall_tex: Texture for horizontal walls.
      - door_closed_img, door_open_img: Images for closed and open door states.
      - walls: List of pygame.Rect objects defining wall positions/sizes.
    """
    # Draw background
    screen.blit(bg_image, (0, 0))
    
    # Render walls with proper texture (vertical or horizontal)
    for wall in walls:
        if wall.width < wall.height:
            texture = vert_wall_tex
        else:
            texture = horiz_wall_tex
        scaled_wall = pygame.transform.scale(texture, (wall.width, wall.height))
        screen.blit(scaled_wall, (wall.x, wall.y))
    
    # Draw coins as yellow squares
    for coin in coins:
        if not coin.collected:
            pygame.draw.rect(screen, (255, 255, 0), (coin.x, coin.y, coin.width, coin.height))
    
    # Draw door: Use door_open_img if unlocked; door_closed_img if locked.
    # We'll scale the door image to 50x80.
    door_image = door_open_img if not door.is_locked else door_closed_img
    scaled_door = pygame.transform.scale(door_image, (50, 80))
    screen.blit(scaled_door, (door.x, door.y))
    
    # Draw player (blue square)
    player.draw(screen)
    
    # Draw the current level timer
    font = pygame.font.SysFont(None, 36)
    timer_text = font.render(f"Time: {int(timer.current_time)}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))
    
    pygame.display.flip()

def render_win_screen(screen, bg_image, total_time, restart_button_rect):
    """
    Renders the win screen with total time and a restart button.
    """
    screen.blit(bg_image, (0, 0))
    
    font = pygame.font.SysFont(None, 48)
    win_text = font.render("You Win!", True, (255, 255, 255))
    time_text = font.render(f"Total Time: {int(total_time)} seconds", True, (255, 255, 255))
    
    win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(win_text, win_rect)
    screen.blit(time_text, time_rect)
    
    pygame.draw.rect(screen, (0, 0, 255), restart_button_rect)
    button_font = pygame.font.SysFont(None, 36)
    button_text = button_font.render("Restart", True, (255, 255, 255))
    btn_text_rect = button_text.get_rect(center=restart_button_rect.center)
    screen.blit(button_text, btn_text_rect)
    
    pygame.display.flip()

def create_coins(coin_positions, walls, coin_width=20, coin_height=20):
    """
    Create Coin objects from given positions.
    If a coin collides with a wall, reposition it up to 100 times.
    """
    coins = []
    for pos in coin_positions:
        x, y = pos
        coin_rect = pygame.Rect(x, y, coin_width, coin_height)
        collision = any(coin_rect.colliderect(wall) for wall in walls)
        attempts = 0
        while collision and attempts < 100:
            x = random.randint(0, SCREEN_WIDTH - coin_width)
            y = random.randint(0, SCREEN_HEIGHT - coin_height)
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
    
    # Load and stretch background image (assumed to be 80x80) to 800x600
    original_bg = pygame.image.load("assets/background.png").convert()
    bg_image = pygame.transform.scale(original_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Load wall textures
    vertical_wall_texture = pygame.image.load("assets/vertical_wall.png").convert()
    horizontal_wall_texture = pygame.image.load("assets/horizontal_wall.png").convert()
    
    # Load door images
    door_closed_img = pygame.image.load("assets/door_closed.png").convert_alpha()
    door_open_img = pygame.image.load("assets/door_open.png").convert_alpha()
    
    # Game state variables
    game_state = "playing"  # "playing" or "win"
    total_time = 0.0
    
    # Initialize level manager and get current level data
    level_manager = LevelManager()
    current_level = level_manager.get_current_level()
    
    # Create level objects:
    walls = [pygame.Rect(x, y, w, h) for (x, y, w, h) in current_level["walls"]]
    player = Player(*current_level["player_start"])
    coins = create_coins(current_level["coins"], walls)
    door = Door(*current_level["door"])
    timer = Timer(current_level["time_limit"])
    
    # Define a restart button rectangle for the win screen
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 50, 120, 50)
    
    running = True
    while running:
        delta_time = clock.get_time() / 1000.0  # in seconds
        if game_state == "playing":
            total_time += delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state == "win" and event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    level_manager.reset()
                    current_level = level_manager.get_current_level()
                    walls = [pygame.Rect(x, y, w, h) for (x, y, w, h) in current_level["walls"]]
                    player.x, player.y = current_level["player_start"]
                    player.rect.topleft = (player.x, player.y)
                    coins = create_coins(current_level["coins"], walls)
                    door.x, door.y = current_level["door"]
                    door.lock()
                    timer.reset(current_level["time_limit"])
                    total_time = 0.0
                    game_state = "playing"
        
        if game_state == "playing":
            direction_vector = get_input()
            prev_x, prev_y = player.x, player.y
            if direction_vector != (0, 0):
                player.move(direction_vector)
            
            # Check wall collisions; revert movement if needed.
            for wall in walls:
                if player.rect.colliderect(wall):
                    player.x, player.y = prev_x, prev_y
                    player.rect.topleft = (player.x, player.y)
                    break
            
            # Enforce screen boundaries
            if player.x < 0:
                player.x = 0
            if player.x + player.width > SCREEN_WIDTH:
                player.x = SCREEN_WIDTH - player.width
            if player.y < 0:
                player.y = 0
            if player.y + player.height > SCREEN_HEIGHT:
                player.y = SCREEN_HEIGHT - player.height
            player.rect.topleft = (player.x, player.y)
            
            # Check coin collisions
            for coin in coins:
                if not coin.collected and coin.check_collision(player):
                    coin.collect()
            
            # Unlock door if all coins are collected
            if all(coin.collected for coin in coins):
                door.unlock()
            
            # Check if player reaches the door
            if door.check_collision(player) and not door.is_locked:
                level_manager.next_level()
                if level_manager.current_level_index >= len(level_manager.levels):
                    game_state = "win"
                else:
                    current_level = level_manager.get_current_level()
                    walls = [pygame.Rect(x, y, w, h) for (x, y, w, h) in current_level["walls"]]
                    player.x, player.y = current_level["player_start"]
                    player.rect.topleft = (player.x, player.y)
                    coins = create_coins(current_level["coins"], walls)
                    door.x, door.y = current_level["door"]
                    door.lock()
                    timer.reset(current_level["time_limit"])
            
            # Update timer; if time runs out, reset coins and door
            if timer.update(delta_time):
                for coin in coins:
                    coin.collected = False
                door.lock()
                timer.reset(current_level["time_limit"])
            
            render_game(
                screen,
                bg_image,
                vertical_wall_texture,
                horizontal_wall_texture,
                door_closed_img,
                door_open_img,
                player,
                coins,
                door,
                timer,
                walls
            )
        
        elif game_state == "win":
            render_win_screen(screen, bg_image, total_time, restart_button)
        
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()