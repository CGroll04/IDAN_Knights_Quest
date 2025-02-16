# src/main.py

import pygame
from level_manager import LevelManager
from player import Player
from objects import Coin, Door
from input_handler import get_input
from utils import Timer

# Screen dimensions (adjust as needed)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def render_game(screen, player, coins, door, timer):
    # Clear screen with a background color (black)
    screen.fill((0, 0, 0))
    
    # Draw coins
    for coin in coins:
        if not coin.collected:
            # Draw coin as a yellow circle
            pygame.draw.circle(screen, (255, 255, 0), (coin.x, coin.y), 10)
    
    # Draw door (green if unlocked, red if locked)
    door_color = (0, 255, 0) if not door.is_locked else (255, 0, 0)
    pygame.draw.rect(screen, door_color, (door.x, door.y, 50, 80))
    
    # Draw player as a blue rectangle
    pygame.draw.rect(screen, (0, 0, 255), (player.x, player.y, 40, 40))
    
    # Draw timer text
    font = pygame.font.SysFont(None, 36)
    timer_text = font.render(f"Time: {int(timer.current_time)}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))
    
    # Refresh display
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("IDAN Pong: Your New Adventure")
    
    clock = pygame.time.Clock()
    
    # Initialize Level Manager with predefined level data
    level_manager = LevelManager()
    current_level = level_manager.get_current_level()
    
    # Create game objects for the level
    # Player: starting position comes from level data
    player = Player(*current_level["player_start"])
    
    # Coins: list of Coin objects using positions from level data
    coins = [Coin(x, y) for x, y in current_level["coins"]]
    
    # Door: door object using position from level data
    door = Door(*current_level["door"])
    
    # Timer: set with the time limit from level data
    timer = Timer(current_level["time_limit"])
    
    running = True
    while running:
        delta_time = clock.get_time() / 1000.0  # Time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get input (keyboard for now; later you can integrate sensor input)
        direction = get_input()
        if direction:
            player.move(direction)
        
        # Check collision between player and each coin
        for coin in coins:
            if not coin.collected and coin.check_collision(player):
                coin.collect()
                # Optional: play a sound or add an effect here
        
        # If all coins collected, unlock the door
        if all(coin.collected for coin in coins):
            door.unlock()
        
        # Check if player reaches the door (simple bounding box collision)
        if door.check_collision(player) and not door.is_locked:
            # Move to next level
            level_manager.next_level()
            current_level = level_manager.get_current_level()
            # Reinitialize objects for the new level
            player.x, player.y = current_level["player_start"]
            coins = [Coin(x, y) for x, y in current_level["coins"]]
            door.x, door.y = current_level["door"]
            door.is_locked = True  # Reset door lock
            timer.reset(current_level["time_limit"])
        
        # Update timer
        if timer.update(delta_time):
            # Timer reached zero: Reset level
            # For simplicity, reinitialize coins and door lock state
            for coin in coins:
                coin.collected = False
            door.lock()
            timer.reset(current_level["time_limit"])
            # Optional: Reset player position if desired
        
        render_game(screen, player, coins, door, timer)
        clock.tick(30)  # 30 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()