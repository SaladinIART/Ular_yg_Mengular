# Main Game Loop
def main():
    """Main game loop"""
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

print("Main Game Loop Module loaded successfully.")