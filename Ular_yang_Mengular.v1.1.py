import pygame
import sys
import random
import os

# Initialization & Setup
pygame.init()
WIDTH, HEIGHT = 1000, 700
GAME_WIDTH, GAME_HEIGHT = 800, 600
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game v1.0")
clock = pygame.time.Clock()
BLACK, WHITE, RED, GREEN, GRAY = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (100, 100, 100)

# High Score Management
def save_high_score(score):
    file_path = os.path.join(os.getcwd(), "high_scores.txt")
    high_scores = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            high_scores = [int(line.strip()) for line in f]
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:5]
    with open(file_path, "w") as f:
        for s in high_scores:
            f.write(f"{s}\n")

def show_high_scores():
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

# Drawing Functions
def draw_grid():
    for x in range(0, GAME_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, GAME_HEIGHT))
    for y in range(0, GAME_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (GAME_WIDTH, y))

# Game Logic
def spawn_food(snake):
    while True:
        x = random.randrange(0, GAME_WIDTH, GRID_SIZE)
        y = random.randrange(0, GAME_HEIGHT, GRID_SIZE)
        if [x, y] not in snake:
            return x, y

def move_snake(snake, dx, dy):
    new_head = [snake[0][0] + dx, snake[0][1] + dy]
    snake.insert(0, new_head)
    return new_head

# Main Game Loop
def main():
    snake = [[GAME_WIDTH // 2, GAME_HEIGHT // 2]]
    dx, dy = GRID_SIZE, 0
    food = spawn_food(snake)
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
        new_head = move_snake(snake, dx, dy)
        if new_head == [food[0], food[1]]:
            score += 1
            food = spawn_food(snake)
        else:
            snake.pop()

        # Check for collisions
        if new_head[0] < 0 or new_head[0] >= GAME_WIDTH or new_head[1] < 0 or new_head[1] >= GAME_HEIGHT or new_head in snake[1:]:
            save_high_score(score)
            if not show_high_scores():
                pygame.quit()
                sys.exit()
            return

        # Drawing
        screen.fill(BLACK)
        draw_grid()
        pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()