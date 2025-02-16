# src/main.py

import pygame
import random
from level_manager import LevelManager
from player import Player  # Player uses knight.png
from objects import Coin, Door
from input_handler import get_input
from utils import Timer

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class MovingObstacle:
    def __init__(self, x, y, width, height, vx, vy, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
        self.image = image

    def update(self, walls):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Bounce off screen boundaries
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vx = -self.vx
            self.rect.x += self.vx
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
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

def create_obstacles(walls, obstacle_image, count=3, obs_width=30, obs_height=30):
    """
    Creates multiple spider obstacles at random positions, avoiding walls.
    We've increased the velocity range to [-4, -3, -2, 2, 3, 4].
    """
    obstacles = []
    possible_speeds = [-4, -3, -2, 2, 3, 4]  # Updated range
    for _ in range(count):
        attempts = 0
        while attempts < 100:
            x = random.randint(0, SCREEN_WIDTH - obs_width)
            y = random.randint(0, SCREEN_HEIGHT - obs_height)
            obs_rect = pygame.Rect(x, y, obs_width, obs_height)
            if not any(obs_rect.colliderect(wall) for wall in walls):
                vx = random.choice(possible_speeds)
                vy = random.choice(possible_speeds)
                obstacle = MovingObstacle(x, y, obs_width, obs_height, vx, vy, obstacle_image)
                obstacles.append(obstacle)
                break
            attempts += 1
        if attempts >= 100:
            print("Failed to place an obstacle without collision; skipping one.")
    return obstacles

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

def create_coins(coin_positions, walls, coin_width=20, coin_height=20):
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
    
    # Always reset the state at startup
    game_state = "playing"
    total_time = 0.0
    
    # Initialize level manager and reset it to ensure starting at level 0
    level_manager = LevelManager()
    level_manager.reset()  # This resets current_level_index to 0
    current_level = level_manager.get_current_level()
    
    original_bg = pygame.image.load("assets/background.png").convert()
    bg_image = pygame.transform.scale(original_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    vertical_wall_texture = pygame.image.load("assets/vertical_wall.png").convert()
    horizontal_wall_texture = pygame.image.load("assets/horizontal_wall.png").convert()
    
    door_closed_img = pygame.image.load("assets/door_closed.png").convert_alpha()
    door_open_img = pygame.image.load("assets/door_open.png").convert_alpha()
    coin_img = pygame.image.load("assets/coin.png").convert_alpha()
    spider_img = pygame.image.load("assets/spider.png").convert_alpha()
    
    game_state = "playing"
    total_time = 0.0
    gameover_reason = ""
    
    level_manager = LevelManager()
    current_level = level_manager.get_current_level()
    
    walls = [pygame.Rect(x, y, w, h) for (x, y, w, h) in current_level["walls"]]
    player = Player(*current_level["player_start"])
    coins = create_coins(current_level["coins"], walls)
    door = Door(*current_level["door"])
    timer = Timer(current_level["time_limit"])
    
    # Create obstacles with faster minimum speed
    obstacles = create_obstacles(walls, spider_img, count=3, obs_width=30, obs_height=30)
    
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
                    coins = create_coins(current_level["coins"], walls)
                    door.x, door.y = current_level["door"]
                    door.lock()
                    timer.reset(current_level["time_limit"])
                    # Recreate obstacles with updated speed range
                    obstacles = create_obstacles(walls, spider_img, count=3, obs_width=30, obs_height=30)
                    total_time = 0.0
                    game_state = "playing"
        
        if game_state == "playing":
            direction_vector = get_input()
            prev_x, prev_y = player.x, player.y
            if direction_vector != (0, 0):
                player.move(direction_vector)
            
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
            
            # Update obstacles & check collision
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
            
            # Check door
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