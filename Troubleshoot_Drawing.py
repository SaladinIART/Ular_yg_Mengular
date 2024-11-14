# Drawing Functions
def draw_grid():
    """Draw the grid on the game area"""
    for x in range(0, GAME_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, GAME_HEIGHT))
    for y in range(0, GAME_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (GAME_WIDTH, y))

# This module should be tested by calling `draw_grid()` within the main game loop
print("Drawing Functions Module loaded successfully.")