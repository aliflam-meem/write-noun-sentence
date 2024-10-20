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

MELTED_SNOWMAN_ID = 5

# Colors
DARK_GRAY = (50, 50, 50)
brown = (205, 133, 63)
saddlebrown = (139, 69, 19)
cornsilk = (251, 245, 229)
BUTTON_FONT_COLOR = (255, 235, 205)
BUTTON_COLOR = (160, 82, 45)
GAME_SCREEN_BG = pygame.image.load("assets/main_bg.jpg")
GAME_SCREEN_BG = pygame.transform.scale(GAME_SCREEN_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
HEALTH_POINT_IMAGE = pygame.image.load("assets/health_heart.png")
SNOWMAN_GAME_RESULT = "assets/game_result_snowman.jpg"

# Create the Pygame screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ألف لام ميم")

# Load fonts
title_font = pygame.font.Font("assets/Shoroq-Font.ttf", 48)
title_font.set_script("Arab")
title_font.set_direction(pygame.DIRECTION_RTL)
subtitle_font = pygame.font.Font("assets/Shoroq-Font.ttf", 35)
subtitle_font.set_script("Arab")
subtitle_font.set_direction(pygame.DIRECTION_RTL)
body_font = pygame.font.Font("assets/Shoroq-Font.ttf", 30)
body_font.set_script("Arab")
body_font.set_direction(pygame.DIRECTION_RTL)
numbering_font = pygame.font.Font("assets/Shoroq-Font.ttf", 30)
numbering_font.set_script("Arab")

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
SNOWMAN_LEVELS = "snowman_levels"
PREPOSITION_GAME = "preposition_game"
VOCABULARY_GAME = "vocabulary_game"
SNOWMAN_GAME = "snowman_game"

# Snowman levels
snowman_levels_keys = ["al_atareef", "demonstratives", "pronouns"]
snowman_levels = {
    snowman_levels_keys[0]: {
        "name": "al_atareef",
        "title": "المعرف بأل التعريف",
        "noun_types": ["اسم ظاهر معرف بـأل التعريف،حالة المفرد",
                       "اسم ظاهر معرف بـأل التعريف،حالة المثنى",
                       "اسم ظاهر معرف بـأل التعريف،حالة جمع المؤنث السالم",
                       "اسم ظاهر معرف بـأل التعريف،حالة جمع المذكر السالم"
                       "اسم ظاهر معرف بـأل التعريف،حالة جمع التكسير"]
    },
    snowman_levels_keys[1]: {
        "name": "demonstratives",
        "title": "اسم الإشارة",
        "noun_types": ["اسم إشارة"]
    },
    snowman_levels_keys[2]: {
        "name": "pronouns",
        "title": "الضمير",
        "noun_types": ["ضمير مفرد", "ضمير مثنى", "ضمير جمع"]
    }
}
