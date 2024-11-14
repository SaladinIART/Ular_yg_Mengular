import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1000, 700
GAME_WIDTH, GAME_HEIGHT = 800, 600
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game v1.1")

# Set up the clock for controlling game speed
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# Define levels with different speeds and obstacles
levels = [
    {"speed": 10, "obstacles": []},
    {"speed": 12, "obstacles": [(200, 200, GRID_SIZE * 2, GRID_SIZE), (400, 300, GRID_SIZE, GRID_SIZE * 3)]},
    {"speed": 15, "obstacles": [(100, 150, GRID_SIZE * 4, GRID_SIZE), (500, 400, GRID_SIZE * 2, GRID_SIZE * 2)]}
]

# High score handling
def save_high_score(score):
    """Save the high score to a text file"""
    file_path = os.path.join(os.getcwd(), "high_scores.txt")
    high_scores = []

    # Read existing high scores if the file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            high_scores = [int(line.strip()) for line in f]

    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:5]  # Keep only top 5 scores

    # Write updated high scores to the file
    with open(file_path, "w") as f:
        for s in high_scores:
            f.write(f"{s}\n")

def show_high_scores():
    """Display the high scores screen"""
    file_path = os.path.join(os.getcwd(), "high_scores.txt")
    high_scores = []

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            high_scores = [line.strip() for line in f]

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

def main():
    """Main game loop"""
    snake = [[GAME_WIDTH // 2, GAME_HEIGHT // 2]]
    dx, dy = GRID_SIZE, 0
    food = spawn_food(snake, [])
    score = 0
    level = 0
    speed = levels[level]["speed"]
    obstacles = [pygame.Rect(*ob) for ob in levels[level]["obstacles"]]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(score)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -GRID_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, GRID_SIZE
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -GRID_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = GRID_SIZE, 0

        # Move the snake
        new_head = [snake[0][0] + dx, snake[0][1] + dy]

        # Check for collisions with the walls
        if new_head[0] < 0 or new_head[0] >= GAME_WIDTH or new_head[1] < 0 or new_head[1] >= GAME_HEIGHT:
            save_high_score(score)
            if not show_high_scores():
                pygame.quit()
                sys.exit()
            return  # Restart the game

        # Check for collisions with itself
        if new_head in snake:
            save_high_score(score)
            if not show_high_scores():
                pygame.quit()
                sys.exit()
            return  # Restart the game

        # Check for collisions with obstacles
        if any(obstacle.collidepoint(new_head[0], new_head[1]) for obstacle in obstacles):
            save_high_score(score)
            if not show_high_scores():
                pygame.quit()
                sys.exit()
            return  # Restart the game

        # Check if the snake eats the food
        if new_head == food:
            score += 1
            food = spawn_food(snake, obstacles)
            # Level up every 5 points, if possible
            if score % 5 == 0 and level < len(levels) - 1:
                level += 1
                speed = levels[level]["speed"]
                obstacles = [pygame.Rect(*ob) for ob in levels[level]["obstacles"]]
        else:
            snake.pop()

        snake.insert(0, new_head)

        # Draw everything
        screen.fill(BLACK)
        draw_grid()
        pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        for obstacle in obstacles:
            pygame.draw.rect(screen, WHITE, obstacle)

        # Display the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (GAME_WIDTH + 20, 10))

        pygame.display.flip()
        clock.tick(speed)

if __name__ == "__main__":
    main()