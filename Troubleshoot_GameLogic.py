# Game Logic
def spawn_food(snake):
    """Spawn food in a random location, avoiding the snake"""
    while True:
        x = random.randrange(0, GAME_WIDTH, GRID_SIZE)
        y = random.randrange(0, GAME_HEIGHT, GRID_SIZE)
        if [x, y] not in snake:
            return x, y

def move_snake(snake, dx, dy):
    """Move the snake and return the new head position"""
    new_head = [snake[0][0] + dx, snake[0][1] + dy]
    snake.insert(0, new_head)
    snake.pop()  # Remove the tail
    return new_head

# This module should be tested with different snake movements and food spawns
print("Game Logic Module loaded successfully.")