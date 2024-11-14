# High Score Management
import os

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

# This module should be tested by calling `save_high_score(score)` and `show_high_scores()`
print("High Score Management Module loaded successfully.")