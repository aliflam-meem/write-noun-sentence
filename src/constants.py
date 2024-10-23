# Constants
import pygame


pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
TITLE_HEIGHT = 100
SCOREBAR_HEIGHT = 60
IMAGE_WIDTH = 500
BUTTON_WIDTH = 220
SMALL_BUTTON_WIDTH = 180
MENU_BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
SMALL_BUTTON_HEIGHT = 50
LONG_PADDING = 100
SMALL_PADDING = 20

# Colors
DARK_GRAY = (50, 50, 50)
brown = (205, 133, 63) #to upper
saddlebrown = (139, 69, 19) #to upper
cornsilk = (251, 245, 229)
BUTTON_FONT_COLOR = (255, 235, 205)
BUTTON_COLOR = (160, 82, 45)
BLACK = (0, 0, 0)

# Images
GAME_SCREEN_BG = pygame.image.load("assets/images/main_bg.jpg")
GAME_SCREEN_BG = pygame.transform.scale(GAME_SCREEN_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
HEALTH_POINT_IMAGE = pygame.image.load("assets/images/health_heart.png")

# Create the Pygame screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ألف لام ميم")

# Load fonts
title_font = pygame.font.Font("assets/fonts/Shoroq-Font.ttf", 48)
title_font.set_script("Arab")
title_font.set_direction(pygame.DIRECTION_RTL)
subtitle_font = pygame.font.Font("assets/fonts/Shoroq-Font.ttf", 35)
subtitle_font.set_script("Arab")
subtitle_font.set_direction(pygame.DIRECTION_RTL)
body_font = pygame.font.Font("assets/fonts/Shoroq-Font.ttf", 30)
body_font.set_script("Arab")
body_font.set_direction(pygame.DIRECTION_RTL)
numbering_font = pygame.font.Font("assets/fonts/Shoroq-Font.ttf", 30)
numbering_font.set_script("Arab")
body_font_bold = pygame.font.Font("assets/fonts/Shoroq-Font.ttf", 30)
body_font_bold.set_script("Arab")
body_font_bold.set_direction(pygame.DIRECTION_RTL)

# Game states
MAIN_MENU = "menu"
GAMES_BOARD_SCREEN = "games_board_screen"
SNOWMAN_LEVELS = "snowman_levels"
PREPOSITION_GAME = "preposition_game"
WHACK_A_MOLE_GAME = "whack_a_mole_game"
SNOWMAN_GAME = "snowman_game"
