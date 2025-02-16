# src/main.py

import pygame
import random
from level_manager import LevelManager
from player import Player  # Player now loads knight.png
from objects import Coin, Door
from input_handler import get_input
from utils import Timer

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the main playable area (invisible boundary) with a margin
MAIN_MARGIN = 50
MAIN_AREA = pygame.Rect(MAIN_MARGIN, MAIN_MARGIN,
                        SCREEN_WIDTH - 2 * MAIN_MARGIN,
                        SCREEN_HEIGHT - 2 * MAIN_MARGIN)

# ---------------------------
# MovingObstacle Class (spider obstacle)
# ---------------------------
class MovingObstacle:
    def __init__(self, x, y, width, height, vx, vy, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
        self.image = image

    def update(self, walls):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Bounce off the main area boundaries
        if self.rect.left < MAIN_AREA.left or self.rect.right > MAIN_AREA.right:
            self.vx = -self.vx
            self.rect.x += self.vx
        if self.rect.top < MAIN_AREA.top or self.rect.bottom > MAIN_AREA.bottom:
            self.vy = -self.vy
            self.rect.y += self.vy

        # Bounce off walls
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

# ---------------------------
# Obstacle Creation Function (choose random positions within MAIN_AREA)
# ---------------------------
def create_obstacles(walls, obstacle_image, count=3, obs_width=30, obs_height=30):
    obstacles = []
    possible_speeds = [-4, -3, -2, 2, 3, 4]  # Increased speed range
    for _ in range(count):
        attempts = 0
        while attempts < 100:
            x = random.randint(MAIN_AREA.left, MAIN_AREA.right - obs_width)
            y = random.randint(MAIN_AREA.top, MAIN_AREA.bottom - obs_height)
            obs_rect = pygame.Rect(x, y, obs_width, obs_height)
            if not any(obs_rect.colliderect(wall) for wall in walls):
                vx = random.choice(possible_speeds)
                vy = random.choice(possible_speeds)
                obstacles.append(MovingObstacle(x, y, obs_width, obs_height, vx, vy, obstacle_image))
                break
            attempts += 1
        if attempts >= 100:
            print("Failed to place an obstacle without collision; skipping one.")
    return obstacles

# ---------------------------
# Render Functions
# ---------------------------
def render_game(screen, bg_image, vert_wall_tex, horiz_wall_tex,
                door_closed_img, door_open_img, coin_img,
                player, coins, door, timer, walls, obstacles):
    screen.blit(bg_image, (0, 0))
    
    # Render walls
    for wall in walls:
        texture = vert_wall_tex if wall.width < wall.height else horiz_wall_tex
        scaled_wall = pygame.transform.scale(texture, (wall.width, wall.height))
        screen.blit(scaled_wall, (wall.x, wall.y))
    
    # Render coins
    for coin in coins:
        if not coin.collected:
            scaled_coin = pygame.transform.scale(coin_img, (coin.width, coin.height))
            screen.blit(scaled_coin, (coin.x, coin.y))
    
    # Render door
    door_image = door_open_img if not door.is_locked else door_closed_img
    scaled_door = pygame.transform.scale(door_image, (50, 80))
    screen.blit(scaled_door, (door.x, door.y))
    
    # Render obstacles (spiders)
    for obstacle in obstacles:
        obstacle.draw(screen)
    
    # Draw player
    player.draw(screen)
    
    # Draw level timer
    font = pygame.font.SysFont(None, 36)
    timer_text = font.render(f"Time: {int(timer.current_time)}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))
    
    pygame.display.flip()

def render_win_screen(screen, bg_image, total_time, restart_button_rect):
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

def render_gameover_screen(screen, bg_image, levels_passed, restart_button_rect, gameover_reason):
    screen.blit(bg_image, (0, 0))
    font = pygame.font.SysFont(None, 48)
    over_text = font.render(gameover_reason, True, (255, 0, 0))
    levels_text = font.render(f"Levels Passed: {levels_passed}", True, (255, 255, 255))
    
    over_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    levels_rect = levels_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(over_text, over_rect)
    screen.blit(levels_text, levels_rect)
    
    pygame.draw.rect(screen, (0, 0, 255), restart_button_rect)
    button_font = pygame.font.SysFont(None, 36)
    button_text = button_font.render("Restart", True, (255, 255, 255))
    btn_text_rect = button_text.get_rect(center=restart_button_rect.center)
    screen.blit(button_text, btn_text_rect)
    
    pygame.display.flip()

# ---------------------------
# Coin Creation Function (ensure placement in MAIN_AREA)
# ---------------------------
def create_coins(coin_positions, walls, coin_width=20, coin_height=20):
    coins = []
    for pos in coin_positions:
        x, y = pos
        # Ensure coin is placed inside MAIN_AREA
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

# ---------------------------
# Main Game Function
# ---------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("IDAN Knight's Quest")
    clock = pygame.time.Clock()
    
    # Load and scale the background image to 800x600
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
    
    # Game state: "playing", "win", "gameover"
    game_state = "playing"
    total_time = 0.0
    gameover_reason = ""
    
    # Initialize level manager and get current level data
    level_manager = LevelManager()
    current_level = level_manager.get_current_level()
    
    # Create level objects
    walls = [pygame.Rect(x, y, w, h) for (x, y, w, h) in current_level["walls"]]
    # Ensure walls are also inside MAIN_AREA (this should be done in level data ideally)
    player = Player(*current_level["player_start"])
    coins = create_coins(current_level["coins"], walls)
    door = Door(*current_level["door"])
    timer = Timer(current_level["time_limit"])
    
    # Create obstacles (spiders) with random positions in MAIN_AREA
    obstacles = create_obstacles(walls, spider_img, count=3, obs_width=30, obs_height=30)
    
    # Define restart button rectangle for win/gameover screens
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 50, 120, 50)
    
    running = True
    while running:
        delta_time = clock.get_time() / 1000.0  # seconds
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
                    coins = create_coins(current_level["coins"], walls)
                    door.x, door.y = current_level["door"]
                    door.lock()
                    timer.reset(current_level["time_limit"])
                    obstacles = create_obstacles(walls, spider_img, count=3, obs_width=30, obs_height=30)
                    total_time = 0.0
                    game_state = "playing"
        
        if game_state == "playing":
            direction_vector = get_input()
            prev_x, prev_y = player.x, player.y
            if direction_vector != (0, 0):
                player.move(direction_vector)
            
            # Check player-wall collisions
            for wall in walls:
                if player.rect.colliderect(wall):
                    player.x, player.y = prev_x, prev_y
                    player.rect.topleft = (player.x, player.y)
                    break
            
            # Enforce boundaries using MAIN_AREA
            if player.x < MAIN_AREA.left:
                player.x = MAIN_AREA.left
            if player.x + player.width > MAIN_AREA.right:
                player.x = MAIN_AREA.right - player.width
            if player.y < MAIN_AREA.top:
                player.y = MAIN_AREA.top
            if player.y + player.height > MAIN_AREA.bottom:
                player.y = MAIN_AREA.bottom - player.height
            player.rect.topleft = (player.x, player.y)
            
            # Update obstacles and check collision with player
            for obstacle in obstacles:
                obstacle.update(walls)
                if player.rect.colliderect(obstacle.rect):
                    game_state = "gameover"
                    gameover_reason = "You Died!"
            
            # Check coin collisions
            for coin in coins:
                if not coin.collected and coin.check_collision(player):
                    coin.collect()
            
            # Unlock door if all coins collected
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
                    obstacles = create_obstacles(walls, spider_img, count=3, obs_width=30, obs_height=30)
            
            # Update timer; if time runs out, gameover
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