# Initialization & Setup
import pygame
import sys
import random

pygame.init()

# Set up the display
WIDTH, HEIGHT = 1000, 700
GAME_WIDTH, GAME_HEIGHT = 800, 600
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game v1.0")

# Set up the clock for controlling game speed
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# This module should initialize without errors
print("Initialization & Setup Module loaded successfully.")