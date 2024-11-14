import pygame
import sys
import random
import json

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1000, 700
GAME_WIDTH, GAME_HEIGHT = 800, 600
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake Game")

# Set up the clock for controlling game speed
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# Define power-up types
SPEED_BOOST = 0
SHIELD = 1
GHOST = 2

# Define levels
levels = [
    {"speed": 10, "obstacles": []},
    {"speed": 12, "obstacles": [(200, 200, 100, 20), (500, 400, 20, 100)]},
    {"speed": 15, "obstacles": [(100, 100, 200, 20), (500, 300, 20, 200), (300, 500, 200, 20)]}
]

def draw_grid():
    """Draw the grid on the game area"""
    for x in range(0, GAME_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, GAME_HEIGHT))
    for y in range(0, GAME_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (GAME_WIDTH, y))

def spawn_food(snake, obstacles):
    """Spawn food in a random location, avoiding the snake and obstacles"""
    while True:
        x = random.randrange(0, GAME_WIDTH, GRID_SIZE)
        y = random.randrange(0, GAME_HEIGHT, GRID_SIZE)
        if [x, y] not in snake and not any(obstacle.collidepoint(x, y) for obstacle in obstacles):
            return x, y

def spawn_power_up(snake, obstacles):
    """Spawn a power-up in a random location, avoiding the snake and obstacles"""
    while True:
        x = random.randrange(0, GAME_WIDTH, GRID_SIZE)
        y = random.randrange(0, GAME_HEIGHT, GRID_SIZE)
        if [x, y] not in snake and not any(obstacle.collidepoint(x, y) for obstacle in obstacles):
            return x, y, random.choice([SPEED_BOOST, SHIELD, GHOST])

def save_high_score(score):
    """Save the high score to a JSON file"""
    try:
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []
    
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:5]  # Keep only top 5 scores

    with open("high_scores.json", "w") as f:
        json.dump(high_scores, f)

def show_high_scores():
    """Display the high scores screen"""
    try:
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []

    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    title = font.render("High Scores", True, WHITE)
    screen.blit(title, (WIDTH // 2 - 70, 50))

    for i, score in enumerate(high_scores):
        text = font.render(f"{i+1}. {score}", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 50, 100 + i * 40))

    instruction = font.render("Press C to continue or Q to quit", True, WHITE)
    screen.blit(instruction, (WIDTH // 2 - 150, HEIGHT - 50))

    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return True
                if event.key == pygame.K_q:
                    return False

def flash_effect(color):
    """Create a flash effect on the screen"""
    flash_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    flash_surface.fill(color)
    for alpha in range(0, 128, 8):
        flash_surface.set_alpha(alpha)
        screen.blit(flash_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5)
    for alpha in range(128, 0, -8):
        flash_surface.set_alpha(alpha)
        screen.blit(flash_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5)

def draw_legend():
    """Draw the legend explaining game elements"""
    font = pygame.font.Font(None, 24)
    legends = [
        ("Snake", GREEN),
        ("Food", RED),
        ("Speed Boost", BLUE),
        ("Shield", PURPLE),
        ("Ghost", WHITE),
        ("Obstacle", GRAY)
    ]
    for i, (text, color) in enumerate(legends):
        pygame.draw.rect(screen, color, (GAME_WIDTH + 20, 50 + i * 30, 20, 20))
        label = font.render(text, True, WHITE)
        screen.blit(label, (GAME_WIDTH + 50, 50 + i * 30))

def draw_pause_menu():
    """Draw the pause menu overlay"""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 48)
    pause_text = font.render("PAUSED", True, WHITE)
    resume_text = font.render("Press ESC to Resume", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)

    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 60))

    pygame.display.flip()

def main():
    """Main game loop"""
    # Initialize game state
    snake = [[GAME_WIDTH // 2, GAME_HEIGHT // 2],
             [GAME_WIDTH // 2 - GRID_SIZE, GAME_HEIGHT // 2],
             [GAME_WIDTH // 2 - 2 * GRID_SIZE, GAME_HEIGHT // 2]]
    dx, dy = GRID_SIZE, 0
    score = 0
    level = 0
    speed = levels[level]["speed"]
    obstacles = [pygame.Rect(ob) for ob in levels[level]["obstacles"]]
    food = spawn_food(snake, obstacles)
    power_up = None
    power_up_timer = 0
    shield_active = False
    ghost_active = False
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(score)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        draw_pause_menu()
                    continue
                if not paused:
                    if event.key == pygame.K_UP and dy == 0:
                        dx, dy = 0, -GRID_SIZE
                    if event.key == pygame.K_DOWN and dy == 0:
                        dx, dy = 0, GRID_SIZE
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx, dy = -GRID_SIZE, 0
                    if event.key == pygame.K_RIGHT and dx == 0:
                        dx, dy = GRID_SIZE, 0
                else:
                    if event.key == pygame.K_q:
                        save_high_score(score)
                        pygame.quit()
                        sys.exit()

        if paused:
            clock.tick(15)
            continue

        # Move snake
        new_head = [(snake[0][0] + dx) % GAME_WIDTH, (snake[0][1] + dy) % GAME_HEIGHT]

        # Check if snake hit the wall
        if new_head[0] in (0, GAME_WIDTH - GRID_SIZE) or new_head[1] in (0, GAME_HEIGHT - GRID_SIZE):
            if not ghost_active:
                flash_effect(YELLOW)
            else:
                ghost_active = False
                flash_effect(WHITE)

        # Check if snake ate food
        if new_head[0] == food[0] and new_head[1] == food[1]:
            snake.insert(0, new_head)
            food = spawn_food(snake, obstacles)
            score += 1
            if score % 5 == 0 and level < len(levels) - 1:
                level += 1
                speed = levels[level]["speed"]
                obstacles = [pygame.Rect(ob) for ob in levels[level]["obstacles"]]
                flash_effect(BLUE)
            if not power_up and random.random() < 0.3:  # 30% chance to spawn power-up
                power_up = spawn_power_up(snake, obstacles)
        else:
            snake.insert(0, new_head)
            snake.pop()

        # Check if snake hit itself
        if new_head in snake[1:]:
            if shield_active:
                shield_active = False
                flash_effect(PURPLE)
            else:
                save_high_score(score)
                if not show_high_scores():
                    pygame.quit()
                    sys.exit()
                return  # Restart the game

        # Check if snake hit obstacle
        for obstacle in obstacles:
            if obstacle.collidepoint(new_head[0], new_head[1]):
                if ghost_active:
                    ghost_active = False
                    flash_effect(WHITE)
                else:
                    save_high_score(score)
                    if not show_high_scores():
                        pygame.quit()
                        sys.exit()
                    return  # Restart the game

        # Check if snake got power-up
        if power_up and new_head[0] == power_up[0] and new_head[1] == power_up[1]:
            if power_up[2] == SPEED_BOOST:
                speed += 2
                flash_effect(BLUE)
            elif power_up[2] == SHIELD:
                shield_active = True
                flash_effect(PURPLE)
            elif power_up[2] == GHOST:
                ghost_active = True
                flash_effect(WHITE)
            power_up = None
            power_up_timer = 100  # Power-up lasts for 100 frames

        if power_up_timer > 0:
            power_up_timer -= 1
            if power_up_timer == 0:
                shield_active = False
                ghost_active = False

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, DARK_GRAY, (0, 0, GAME_WIDTH, GAME_HEIGHT))
        draw_grid()
        for segment in snake:
            pygame.draw.rect(screen, GREEN if not shield_active else PURPLE, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))
        for obstacle in obstacles:
            pygame.draw.rect(screen, GRAY, obstacle)
        if power_up:
            color = BLUE if power_up[2] == SPEED_BOOST else (PURPLE if power_up[2] == SHIELD else WHITE)
            pygame.draw.rect(screen, color, (power_up[0], power_up[1], GRID_SIZE, GRID_SIZE))

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (GAME_WIDTH + 20, 10))

        # Display level at bottom right, outside game area
        level_text = font.render(f"Level: {level + 1}", True, WHITE)
        level_text_rect = level_text.get_rect()
        level_text_rect.bottomright = (WIDTH - 10, HEIGHT - 10)
        screen.blit(level_text, level_text_rect)

        draw_legend()

        pygame.display.flip()
        clock.tick(speed)

if __name__ == "__main__":
    while True:
        main()