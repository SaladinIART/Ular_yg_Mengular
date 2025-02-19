Snake Game Documentation

Overview

Project Name: Ular_yg_MengularDescription: A Python-based snake game that evolves over time, incorporating features like high scores, real-time score display, and modular code organization. This project is aimed at creating an engaging and feature-rich gaming experience.

Features

Core Gameplay:

Classic snake game mechanics where the snake grows when it eats food.

Game ends when the snake collides with the walls or itself.

High Score Management:

High scores are stored in a JSON file (high_scores.json).

Displays the top 5 high scores after each game.

Pause Functionality:

Players can pause the game using the spacebar.

A semi-transparent overlay with a "Game Paused" message appears during the pause.

Real-Time Score Display:

A side panel shows the current score, session high score, and game instructions.

Customizable Grid and Game Area:

Adjustable grid size and game area dimensions.

Modular Code Design:

Game logic is split into multiple modules for easier troubleshooting and future enhancements.

File Structure

Ular_yg_Mengular/
├── Troubleshoot_Drawing.py       # Troubleshooting for drawing-related issues
├── Troubleshoot_GameLogic.py     # Troubleshooting for game logic issues
├── Troubleshoot_HighScore.py     # Troubleshooting for high score issues
├── Troubleshoot_Init.py          # Troubleshooting for initialization issues
├── Troubleshoot_MainGameLoop.py  # Troubleshooting for main game loop issues
├── Ular_yang_Mengular.v1.0.py    # First attempt of the game
├── Ular_yang_Mengular.v1.1.py    # Improved version with high scores
├── LICENSE                       # MIT License
├── README.md                     # Project description

How to Run the Game

Requirements:

Python 3.8 or higher

pygame library

Installation:

pip install pygame

Running the Game:

python Ular_yang_Mengular.v1.1.py

Modules and Their Functions

1. Troubleshoot_Drawing.py

Handles drawing functions like the grid, snake, food, and side panel.

2. Troubleshoot_GameLogic.py

Manages game logic, including:

Snake movement.

Food spawning.

Collision detection.

3. Troubleshoot_HighScore.py

Manages high score storage and retrieval.

Saves high scores in high_scores.json.

4. Troubleshoot_Init.py

Handles initialization tasks like setting up the game window and grid.

5. Troubleshoot_MainGameLoop.py

Contains the main game loop.

Handles event processing, snake movement, and game state updates.

Features in Detail

High Score Management

File Format: JSON (high_scores.json)

Schema:

[
  {
    "score": 10,
    "player": "Player",
    "timestamp": 1678901234
  }
]

Functions:

load_high_scores(): Loads high scores from the JSON file.

save_high_score(score): Saves the new score if it qualifies for the top 5.

Real-Time Score Display

A side panel displays:

Current score.

Session high score.

Instructions for controlling the game.

Implemented in the draw_side_panel() function.

Pause Functionality

Pauses the game when the spacebar is pressed.

Displays a semi-transparent overlay with a "Game Paused" message.

Resumes the game when "C" is pressed.

Future Enhancements

Dynamic Difficulty:

Increase snake speed as the score increases.

Power-Ups:

Add power-ups like speed boosts or extra points.

Multiplayer Mode:

Introduce a second snake controlled by another player.

Customization Options:

Allow players to adjust grid size and snake speed.

Enhanced Graphics:

Add animations and textures for the snake and food.

Timer Mode:

Add a game mode with a countdown timer for extra challenge.

License

This project is licensed under the MIT License. See the LICENSE file for more details.

Contributors

SaladinIART: Initial development and troubleshooting.

For further questions or contributions, please refer to the GitHub repository.

