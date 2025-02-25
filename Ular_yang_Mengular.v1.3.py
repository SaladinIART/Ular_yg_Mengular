import pygame
import sys
import random
import os
import json
import time

# Game Configuration
class Config:
    def __init__(self):
        # Optimized for 1920x1200 resolution
        self.WIDTH = 1400
        self.HEIGHT = 900
        self.GAME_WIDTH = 1100
        self.GAME_HEIGHT = 800
        self.GRID_SIZE = 25
        self.FPS = 10
        self.DIFFICULTY_SPEEDS = {
            "Easy": 8,
            "Medium": 12,
            "Hard": 16
        }
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        self.GRAY = (100, 100, 100)
        # Power-up settings
        self.POWERUP_CHANCE = 0.1  # 10% chance of spawning a power-up when food is eaten
        self.POWERUP_DURATION = 5  # 5 seconds

# Game state management
class GameState:
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

class PowerUp:
    def __init__(self, x, y, type_id):
        self.x = x
        self.y = y
        self.type = type_id
        self.active = False
        self.start_time = 0
        self.duration = 0

    def activate(self, duration):
        self.active = True
        self.start_time = time.time()
        self.duration = duration

    def is_expired(self):
        if not self.active:
            return False
        return time.time() - self.start_time > self.duration

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        pygame.display.set_caption("Ular yang Mengular v2.0")
        self.clock = pygame.time.Clock()

        # Game state
        self.state = GameState.MENU
        self.difficulty = "Medium"

        # Power-up initialization - explicitly set to None at start
        self.power_up = None
        self.current_power_up = None

        # Initialize game elements
        self.reset_game()

        # Load high scores
        self.high_scores = self.load_high_scores()
        self.session_high_score = 0

    def reset_game(self):
        # Snake initialization
        self.snake = [[self.config.GAME_WIDTH // 2, self.config.GAME_HEIGHT // 2]]
        self.dx, self.dy = self.config.GRID_SIZE, 0
        self.score = 0

        # Food and power-ups - explicitly set power_up to None
        self.food = self.spawn_food()
        self.power_up = None
        self.current_power_up = None

        # Game options
        self.speed_multiplier = 1.0
        self.growth_factor = 1

    def spawn_food(self):
        while True:
            x = random.randrange(0, self.config.GAME_WIDTH, self.config.GRID_SIZE)
            y = random.randrange(0, self.config.GAME_HEIGHT, self.config.GRID_SIZE)
            # Fixed the power_up check to handle None case properly
            if [x, y] not in self.snake and (self.power_up is None or [x, y] != [self.power_up.x, self.power_up.y]):
                return x, y

    def spawn_power_up(self):
        if random.random() < self.config.POWERUP_CHANCE:
            while True:
                x = random.randrange(0, self.config.GAME_WIDTH, self.config.GRID_SIZE)
                y = random.randrange(0, self.config.GAME_HEIGHT, self.config.GRID_SIZE)
                if [x, y] not in self.snake and (x, y) != self.food:
                    # Random power-up type (0: Speed Boost, 1: Double Points, 2: Shield)
                    power_up_type = random.randint(0, 2)
                    return PowerUp(x, y, power_up_type)
        return None

    def apply_power_up(self, power_up_type):
        if power_up_type == 0:  # Speed Boost
            self.speed_multiplier = 1.5
        elif power_up_type == 1:  # Double Points
            self.growth_factor = 2
        elif power_up_type == 2:  # Shield (implemented in collision detection)
            pass

        self.current_power_up = power_up_type
        self.power_up.activate(self.config.POWERUP_DURATION)

    def check_power_up_expiry(self):
        if self.power_up and self.power_up.active and self.power_up.is_expired():
            # Reset effects
            self.speed_multiplier = 1.0
            self.growth_factor = 1
            self.current_power_up = None
            self.power_up.active = False

    def move_snake(self):
        new_head = [self.snake[0][0] + self.dx, self.snake[0][1] + self.dy]
        self.snake.insert(0, new_head)
        return new_head

    def check_collision(self):
        head = self.snake[0]

        # Check if snake hits the boundary
        if (head[0] < 0 or head[0] >= self.config.GAME_WIDTH or
            head[1] < 0 or head[1] >= self.config.GAME_HEIGHT):
            # Shield power-up lets you pass through walls once
            if self.current_power_up == 2:
                # Wrap around to the other side
                if head[0] < 0:
                    self.snake[0][0] = self.config.GAME_WIDTH - self.config.GRID_SIZE
                elif head[0] >= self.config.GAME_WIDTH:
                    self.snake[0][0] = 0
                elif head[1] < 0:
                    self.snake[0][1] = self.config.GAME_HEIGHT - self.config.GRID_SIZE
                elif head[1] >= self.config.GAME_HEIGHT:
                    self.snake[0][1] = 0

                # Consume the shield
                self.current_power_up = None
                self.power_up.active = False
                self.speed_multiplier = 1.0
                return False
            return True

        # Check if snake hits itself
        if head in self.snake[1:]:
            if self.current_power_up == 2:  # Shield protects from self-collision too
                self.current_power_up = None
                self.power_up.active = False
                self.speed_multiplier = 1.0
                return False
            return True

        return False

    def load_high_scores(self):
        file_path = os.path.join(os.getcwd(), "high_scores.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_high_score(self):
        file_path = os.path.join(os.getcwd(), "high_scores.json")

        # Create a new entry
        entry = {
            "score": self.score,
            "player": "Player",
            "timestamp": int(time.time())
        }

        # Add to high scores and sort
        self.high_scores.append(entry)
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)

        # Keep only top 5
        self.high_scores = self.high_scores[:5]

        # Save to file
        with open(file_path, "w") as f:
            json.dump(self.high_scores, f)

        # Update session high score
        self.session_high_score = max(self.session_high_score, self.score)

    def draw_menu(self):
        self.screen.fill(self.config.BLACK)

        # Title
        font_large = pygame.font.Font(None, 72)
        title = font_large.render("ULAR YANG MENGULAR", True, self.config.GREEN)
        self.screen.blit(title, (self.config.WIDTH // 2 - title.get_width() // 2, 100))

        # Menu options
        font = pygame.font.Font(None, 36)

        # Difficulty selection
        difficulty_text = font.render(f"Difficulty: < {self.difficulty} >", True, self.config.WHITE)
        self.screen.blit(difficulty_text, (self.config.WIDTH // 2 - difficulty_text.get_width() // 2, 250))

        # Start game button
        pygame.draw.rect(self.screen, self.config.GREEN,
                         (self.config.WIDTH // 2 - 100, 320, 200, 50),
                         border_radius=5)
        start_text = font.render("Start Game", True, self.config.BLACK)
        self.screen.blit(start_text, (self.config.WIDTH // 2 - start_text.get_width() // 2, 335))

        # High scores button
        pygame.draw.rect(self.screen, self.config.BLUE,
                         (self.config.WIDTH // 2 - 100, 390, 200, 50),
                         border_radius=5)
        high_scores_text = font.render("High Scores", True, self.config.BLACK)
        self.screen.blit(high_scores_text, (self.config.WIDTH // 2 - high_scores_text.get_width() // 2, 405))

        # Quit button
        pygame.draw.rect(self.screen, self.config.RED,
                         (self.config.WIDTH // 2 - 100, 460, 200, 50),
                         border_radius=5)
        quit_text = font.render("Quit", True, self.config.BLACK)
        self.screen.blit(quit_text, (self.config.WIDTH // 2 - quit_text.get_width() // 2, 475))

        # Instructions
        instruction_text = font.render("Use arrow keys to navigate, SPACE to select", True, self.config.GRAY)
        self.screen.blit(instruction_text, (self.config.WIDTH // 2 - instruction_text.get_width() // 2, 550))

        pygame.display.flip()

    def draw_game(self):
        self.screen.fill(self.config.BLACK)

        # Draw grid
        for x in range(0, self.config.GAME_WIDTH, self.config.GRID_SIZE):
            pygame.draw.line(self.screen, self.config.GRAY, (x, 0), (x, self.config.GAME_HEIGHT))
        for y in range(0, self.config.GAME_HEIGHT, self.config.GRID_SIZE):
            pygame.draw.line(self.screen, self.config.GRAY, (0, y), (self.config.GAME_WIDTH, y))

        # Draw food
        pygame.draw.rect(self.screen, self.config.RED,
                         (self.food[0], self.food[1], self.config.GRID_SIZE, self.config.GRID_SIZE))

        # Draw power-up if exists
        if self.power_up and not self.power_up.active:
            color = self.config.YELLOW if self.power_up.type == 0 else \
                    self.config.PURPLE if self.power_up.type == 1 else \
                    self.config.BLUE
            pygame.draw.rect(self.screen, color,
                            (self.power_up.x, self.power_up.y, self.config.GRID_SIZE, self.config.GRID_SIZE))

        # Draw snake
        for i, segment in enumerate(self.snake):
            # Head in a different color
            if i == 0:
                color = self.config.GREEN
            else:
                # Body segments have a gradient effect
                green_val = max(0, 255 - i * 5)
                color = (0, green_val, 0)

            pygame.draw.rect(self.screen, color,
                            (segment[0], segment[1], self.config.GRID_SIZE, self.config.GRID_SIZE))

        # Draw side panel
        self.draw_side_panel()

        pygame.display.flip()

    def draw_side_panel(self):
        panel_x = self.config.GAME_WIDTH + 10
        panel_width = self.config.WIDTH - self.config.GAME_WIDTH - 20

        # Panel background
        pygame.draw.rect(self.screen, self.config.GRAY,
                         (panel_x, 10, panel_width, self.config.GAME_HEIGHT - 20),
                         border_radius=5)

        # Game info
        font = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)

        # Score
        score_text = font.render(f"Score: {self.score}", True, self.config.WHITE)
        self.screen.blit(score_text, (panel_x + 20, 30))

        # Session high score
        high_score_text = font.render(f"High: {self.session_high_score}", True, self.config.WHITE)
        self.screen.blit(high_score_text, (panel_x + 20, 70))

        # Difficulty
        difficulty_text = font.render(f"Difficulty: {self.difficulty}", True, self.config.WHITE)
        self.screen.blit(difficulty_text, (panel_x + 20, 110))

        # Active power-up
        if self.current_power_up is not None:
            power_up_name = ["Speed Boost", "Double Points", "Shield"][self.current_power_up]
            time_left = max(0, self.config.POWERUP_DURATION - (time.time() - self.power_up.start_time))

            power_up_text = font.render(f"Power-up:", True, self.config.YELLOW)
            self.screen.blit(power_up_text, (panel_x + 20, 160))

            power_up_name_text = font.render(power_up_name, True, self.config.YELLOW)
            self.screen.blit(power_up_name_text, (panel_x + 20, 190))

            time_text = font.render(f"Time: {time_left:.1f}s", True, self.config.YELLOW)
            self.screen.blit(time_text, (panel_x + 20, 220))

        # Controls
        controls_y = 300
        controls_text = font.render("Controls:", True, self.config.WHITE)
        self.screen.blit(controls_text, (panel_x + 20, controls_y))

        controls = [
            "Arrows: Move Snake",
            "Space: Pause",
            "Esc: Quit to Menu"
        ]

        for i, control in enumerate(controls):
            control_text = font_small.render(control, True, self.config.WHITE)
            self.screen.blit(control_text, (panel_x + 20, controls_y + 40 + i * 30))

        # Power-ups legend
        legend_y = 450
        legend_text = font.render("Power-ups:", True, self.config.WHITE)
        self.screen.blit(legend_text, (panel_x + 20, legend_y))

        legends = [
            ("Yellow", "Speed Boost"),
            ("Purple", "Double Points"),
            ("Blue", "Shield")
        ]

        for i, (color_name, effect) in enumerate(legends):
            color = self.config.YELLOW if color_name == "Yellow" else \
                    self.config.PURPLE if color_name == "Purple" else \
                    self.config.BLUE

            pygame.draw.rect(self.screen, color, (panel_x + 20, legend_y + 40 + i * 30, 15, 15))
            legend_item_text = font_small.render(f": {effect}", True, self.config.WHITE)
            self.screen.blit(legend_item_text, (panel_x + 45, legend_y + 38 + i * 30))

    def pause_game(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((self.config.WIDTH, self.config.HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(self.config.BLACK)
        self.screen.blit(overlay, (0, 0))

        # Display pause text
        font = pygame.font.Font(None, 48)
        pause_text = font.render("Game Paused", True, self.config.WHITE)
        continue_text = font.render("Press C to Continue", True, self.config.WHITE)
        quit_text = font.render("Press Q to Quit", True, self.config.WHITE)

        self.screen.blit(pause_text, (self.config.WIDTH // 2 - pause_text.get_width() // 2, self.config.HEIGHT // 2 - 60))
        self.screen.blit(continue_text, (self.config.WIDTH // 2 - continue_text.get_width() // 2, self.config.HEIGHT // 2))
        self.screen.blit(quit_text, (self.config.WIDTH // 2 - quit_text.get_width() // 2, self.config.HEIGHT // 2 + 60))

        pygame.display.flip()

    def show_high_scores(self):
        self.screen.fill(self.config.BLACK)

        # Title
        font = pygame.font.Font(None, 48)
        title = font.render("High Scores", True, self.config.WHITE)
        self.screen.blit(title, (self.config.WIDTH // 2 - title.get_width() // 2, 50))

        # Display high scores
        font = pygame.font.Font(None, 36)
        y_pos = 120

        if not self.high_scores:
            no_scores_text = font.render("No high scores yet!", True, self.config.WHITE)
            self.screen.blit(no_scores_text, (self.config.WIDTH // 2 - no_scores_text.get_width() // 2, y_pos))
        else:
            for i, entry in enumerate(self.high_scores):
                score_text = font.render(f"{i+1}. {entry['score']} points", True, self.config.WHITE)
                self.screen.blit(score_text, (self.config.WIDTH // 2 - 120, y_pos))

                # Convert timestamp to readable date if available
                if 'timestamp' in entry:
                    date = time.strftime('%Y-%m-%d', time.localtime(entry['timestamp']))
                    date_text = font.render(date, True, self.config.GRAY)
                    self.screen.blit(date_text, (self.config.WIDTH // 2 + 80, y_pos))

                y_pos += 50

        # Back button
        pygame.draw.rect(self.screen, self.config.RED,
                         (self.config.WIDTH // 2 - 100, self.config.HEIGHT - 100, 200, 50),
                         border_radius=5)
        back_text = font.render("Back", True, self.config.BLACK)
        self.screen.blit(back_text, (self.config.WIDTH // 2 - back_text.get_width() // 2, self.config.HEIGHT - 85))

        pygame.display.flip()

        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        waiting = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if back button is clicked
                    if (self.config.WIDTH // 2 - 100 <= mouse_pos[0] <= self.config.WIDTH // 2 + 100 and
                        self.config.HEIGHT - 100 <= mouse_pos[1] <= self.config.HEIGHT - 50):
                        waiting = False

    def game_over(self):
        self.save_high_score()

        # Game over screen
        overlay = pygame.Surface((self.config.WIDTH, self.config.HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(self.config.BLACK)
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, 72)
        font = pygame.font.Font(None, 36)

        game_over_text = font_large.render("GAME OVER", True, self.config.RED)
        score_text = font.render(f"Your Score: {self.score}", True, self.config.WHITE)

        continue_text = font.render("Press SPACE to Play Again", True, self.config.WHITE)
        menu_text = font.render("Press ESC for Main Menu", True, self.config.WHITE)

        self.screen.blit(game_over_text,
                         (self.config.WIDTH // 2 - game_over_text.get_width() // 2, self.config.HEIGHT // 2 - 100))
        self.screen.blit(score_text,
                         (self.config.WIDTH // 2 - score_text.get_width() // 2, self.config.HEIGHT // 2 - 20))
        self.screen.blit(continue_text,
                         (self.config.WIDTH // 2 - continue_text.get_width() // 2, self.config.HEIGHT // 2 + 40))
        self.screen.blit(menu_text,
                         (self.config.WIDTH // 2 - menu_text.get_width() // 2, self.config.HEIGHT // 2 + 80))

        pygame.display.flip()

        # Wait for player decision
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        self.reset_game()
                        self.state = GameState.PLAYING
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        # Return to menu
                        self.state = GameState.MENU
                        waiting = False

    def handle_menu_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard navigation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Change difficulty
                    difficulties = list(self.config.DIFFICULTY_SPEEDS.keys())
                    current_index = difficulties.index(self.difficulty)
                    self.difficulty = difficulties[(current_index - 1) % len(difficulties)]

                elif event.key == pygame.K_RIGHT:
                    # Change difficulty
                    difficulties = list(self.config.DIFFICULTY_SPEEDS.keys())
                    current_index = difficulties.index(self.difficulty)
                    self.difficulty = difficulties[(current_index + 1) % len(difficulties)]

                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Start game with current settings
                    self.reset_game()
                    self.state = GameState.PLAYING

            # Mouse interaction
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Start Game button
                if (self.config.WIDTH // 2 - 100 <= mouse_pos[0] <= self.config.WIDTH // 2 + 100 and
                    320 <= mouse_pos[1] <= 370):
                    self.reset_game()
                    self.state = GameState.PLAYING

                # High Scores button
                elif (self.config.WIDTH // 2 - 100 <= mouse_pos[0] <= self.config.WIDTH // 2 + 100 and
                      390 <= mouse_pos[1] <= 440):
                    self.show_high_scores()

                # Quit button
                elif (self.config.WIDTH // 2 - 100 <= mouse_pos[0] <= self.config.WIDTH // 2 + 100 and
                      460 <= mouse_pos[1] <= 510):
                    pygame.quit()
                    sys.exit()

    def handle_gameplay_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.dy == 0:
                    self.dx, self.dy = 0, -self.config.GRID_SIZE
                elif event.key == pygame.K_DOWN and self.dy == 0:
                    self.dx, self.dy = 0, self.config.GRID_SIZE
                elif event.key == pygame.K_LEFT and self.dx == 0:
                    self.dx, self.dy = -self.config.GRID_SIZE, 0
                elif event.key == pygame.K_RIGHT and self.dx == 0:
                    self.dx, self.dy = self.config.GRID_SIZE, 0
                elif event.key == pygame.K_SPACE:
                    self.state = GameState.PAUSED
                elif event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU

    def handle_pause_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_q:
                    self.state = GameState.MENU

    def update_game(self):
        # Check for power-up expiry
        self.check_power_up_expiry()

        # Move the snake
        new_head = self.move_snake()

        # Check if snake eats food
        if new_head == [self.food[0], self.food[1]]:
            self.score += 1 * self.growth_factor
            self.food = self.spawn_food()

            # Potentially spawn a power-up
            if not self.power_up or self.power_up.active:
                self.power_up = self.spawn_power_up()
        else:
            # Only remove the tail if no food was eaten
            self.snake.pop()

        # Check if snake gets power-up
        if self.power_up and not self.power_up.active and new_head == [self.power_up.x, self.power_up.y]:
            self.apply_power_up(self.power_up.type)

        # Check for collisions
        if self.check_collision():
            self.state = GameState.GAME_OVER

    def run(self):
        running = True
        while running:
            if self.state == GameState.MENU:
                self.handle_menu_input()
                self.draw_menu()

            elif self.state == GameState.PLAYING:
                self.handle_gameplay_input()
                self.update_game()
                self.draw_game()

            elif self.state == GameState.PAUSED:
                self.handle_pause_input()
                self.pause_game()

            elif self.state == GameState.GAME_OVER:
                self.game_over()

            # Control game speed based on difficulty and power-ups
            fps = self.config.DIFFICULTY_SPEEDS[self.difficulty] * self.speed_multiplier
            self.clock.tick(fps)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()