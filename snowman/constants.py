# Constants
import pygame


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
TITLE_HEIGHT = 100
IMAGE_WIDTH = 200
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 50
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 60
LONG_PADDING = 100
SMALL_PADDING = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
brown = (205,133,63)
saddlebrown = (139, 69, 19)
BUTTON_FONT_COLOR = (255,235,205)
BUTTON_COLOR = (160,82,45)
GAME_SCREEN_BG = pygame.image.load("main_bg.jpg")
GAME_SCREEN_BG = pygame.transform.scale(GAME_SCREEN_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create the Pygame screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ألف لام ميم")

# Load fonts
title_font = pygame.font.Font("Shoroq-Font.ttf", 48)
title_font.set_script("Arab")
title_font.set_direction(pygame.DIRECTION_RTL)
subtitle_font = pygame.font.Font("Shoroq-Font.ttf", 35)
subtitle_font.set_script("Arab")
subtitle_font.set_direction(pygame.DIRECTION_RTL)
body_font = pygame.font.Font("Shoroq-Font.ttf", 30)
body_font.set_script("Arab")
body_font.set_direction(pygame.DIRECTION_RTL)

# Load images (You would load your own image files here)
# For demonstration purposes, let's assume we have 5 images loaded
# Replace the "image_path" with actual image paths
images = [
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT / 2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT / 2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT / 2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT / 2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT / 2))  # Placeholder surface as an image
]

# Game states
MAIN_MENU = "menu"
GAMES_BOARD_SCREEN = "games_board_screen"
SNOWMAN_GAME = "snowman_game"
PREPOSITION_GAME = "preposition_game"
VOCABULARY_GAME = "vocabulary_game"
