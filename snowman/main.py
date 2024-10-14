import pygame
import sys


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
TITLE_HEIGHT = 100
IMAGE_WIDTH = 200
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 50
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 50
LONG_PADDING = 60
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
title_font = pygame.font.Font("Arial.ttf", 48)
title_font.set_script("Arab")
title_font.set_direction(pygame.DIRECTION_RTL)
subtitle_font = pygame.font.Font("Arial.ttf", 35)
subtitle_font.set_script("Arab")
subtitle_font.set_direction(pygame.DIRECTION_RTL)
body_font = pygame.font.Font("Arial.ttf", 30)
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


# Function to draw the title with background
def draw_title(title, color= BUTTON_FONT_COLOR):
    title_background_rect = pygame.Rect(0, 0, SCREEN_WIDTH, TITLE_HEIGHT)
    pygame.draw.rect(screen, DARK_GRAY, title_background_rect)

    title_text = title_font.render(title, True, color)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, TITLE_HEIGHT // 2))
    screen.blit(title_text, title_rect)


def draw_subtitle(subtitle, x, y, color="white"):
    title_text = subtitle_font.render(subtitle, True, color)
    title_rect = title_text.get_rect()
    title_rect.topright = (x,y)
    screen.blit(title_text, title_rect)


def draw_button(text, x, y, width, height, border_width=2, border_color=saddlebrown, text_color = BUTTON_FONT_COLOR, highlight_color=brown, radius=10):
    """
    Draws a button with rounded corners.

    Args:
        text (str): The text to display on the button.
        x (int): The x-coordinate of the button's top-left corner.
        y (int): The y-coordinate of the button's top-left corner.
        width (int): The width of the button.
        height (int): The height of the button.
        border_width (int, optional): The width of the button's border. Defaults to 2.
        border_color (tuple, optional): The color of the button's border. Defaults to GRAY.
        highlight_color (tuple, optional): The color to use when the button is hovered over. Defaults to saddlebrown.
        radius (int, optional): The radius of the rounded corners. Defaults to 10.
    """

    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    # Draw border
    pygame.draw.rect(screen, border_color, button_rect, border_width, border_radius=radius)

    # Change button color based on hover
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, highlight_color,
                         (x + border_width, y + border_width, width - 2 * border_width, height - 2 * border_width), 0,
                         border_radius=radius)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR,
                         (x + border_width, y + border_width, width - 2 * border_width, height - 2 * border_width), 0,
                         border_radius=radius)

    # Draw button text
    button_text = body_font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    return button_rect


# Dummy action to switch to a new screen (the game screen)
def start_game():
    global game_state
    game_state = GAMES_BOARD_SCREEN


# Action to quit the game
def quit_game():
    pygame.quit()
    sys.exit()


# Function to handle the game screen
def games_board_screen():
    screen.blit(GAME_SCREEN_BG, (0, 0))
    draw_title("قائمة الألعاب")

    # Draw a "Back to Menu" button
    back_button = draw_button("رجوع", 30, (TITLE_HEIGHT - MENU_BUTTON_HEIGHT) / 2, MENU_BUTTON_WIDTH - LONG_PADDING,
                              MENU_BUTTON_HEIGHT)

    # List the games buttons
    space_between_buttons = 20  # space between buttons
    edge_space = (SCREEN_WIDTH - (
        BUTTON_WIDTH * 3 + space_between_buttons * 2)) / 2  # space between screen edges and buttons

    # y-coordinate is the same for all buttons, vertically centered
    y_coordinate = SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT // 2

    # x-coordinates based on edge_space and space_between_buttons
    vocabulary_button_x = SCREEN_WIDTH - edge_space - BUTTON_WIDTH
    prepositions_button_x = vocabulary_button_x - BUTTON_WIDTH - space_between_buttons
    snowman_button_x = prepositions_button_x - BUTTON_WIDTH - space_between_buttons

    # Draw buttons
    vocabulary_button = draw_button("إصابة القنفذ", vocabulary_button_x, y_coordinate, BUTTON_WIDTH,
                                    MENU_BUTTON_HEIGHT)
    prepositions_button = draw_button("بينغو", prepositions_button_x, y_coordinate, BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
    snowman_button = draw_button("الرجل الثلجي", snowman_button_x, y_coordinate, BUTTON_WIDTH, MENU_BUTTON_HEIGHT)

    return back_button, vocabulary_button, prepositions_button, snowman_button


def snowman_levels_screen():
    screen.blit(GAME_SCREEN_BG, (0, 0))
    draw_title("لعبة الرجل الثلجي")

    # List the games buttons
    space_between_buttons = 20  # space between buttons
    edge_space = (SCREEN_WIDTH - (
        BUTTON_WIDTH * 3 + space_between_buttons * 2)) / 2  # space between screen edges and buttons

    # y-coordinate is the same for all buttons, vertically centered
    y_coordinate = SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT // 2

    # x-coordinates based on edge_space and space_between_buttons
    al_atareef_button_x = SCREEN_WIDTH - edge_space - BUTTON_WIDTH
    demonstratives_button_x = al_atareef_button_x - BUTTON_WIDTH - space_between_buttons
    pronouns_button_x = demonstratives_button_x - BUTTON_WIDTH - space_between_buttons

    back_button = draw_button("رجوع", 30, (TITLE_HEIGHT - MENU_BUTTON_HEIGHT) / 2, BUTTON_WIDTH - LONG_PADDING,
                              MENU_BUTTON_HEIGHT)
    # 10 pixels is a magic number, right indent
    draw_subtitle("أشكال المبتدأ", SCREEN_WIDTH - edge_space - 10, y_coordinate - 70, brown)

    # Draw menu buttons
    al_atareef_button = draw_button("المعرف بأل التعريف", al_atareef_button_x, y_coordinate, BUTTON_WIDTH,
                                    MENU_BUTTON_HEIGHT)
    demonstratives_button = draw_button("اسم الإشارة", demonstratives_button_x, y_coordinate, BUTTON_WIDTH,
                                        MENU_BUTTON_HEIGHT)
    pronouns_button = draw_button("الضمير", pronouns_button_x, y_coordinate, BUTTON_WIDTH, MENU_BUTTON_HEIGHT)

    return back_button


def main_menu_screen():
    screen.blit(GAME_SCREEN_BG, (0, 0))
    draw_title("ألف لام ميم")

    # Draw menu buttons
    button_start = draw_button("الألعاب", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                               SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT - SMALL_PADDING, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
    button_options = draw_button("الإعدادات", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                                 SCREEN_HEIGHT // 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
    button_quit = draw_button("الخروج", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                              SCREEN_HEIGHT // 2 + MENU_BUTTON_HEIGHT + SMALL_PADDING, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)

    return button_start, button_options, button_quit


# Main game loop
def main():
    global game_state
    game_state = MAIN_MENU  # Start with the menu screen
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)  # Set background color of the screen

        # Handle different screens based on game state
        if game_state == MAIN_MENU:
            button_start, button_options, button_quit = main_menu_screen()

            # Event handling for menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    if button_start.collidepoint(event.pos):
                        start_game()  # Switch to game screen
                    elif button_options.collidepoint(event.pos):
                        pass
                    elif button_quit.collidepoint(event.pos):
                        quit_game()

        elif game_state == GAMES_BOARD_SCREEN:
            # Display the game screen
            back_button, vocabulary_button, prepositions_button, snowman_button = games_board_screen()

            # Event handling for the game screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    if back_button.collidepoint(event.pos):
                        game_state = MAIN_MENU  # Switch back to the menu
                    if snowman_button.collidepoint(event.pos):
                        game_state = SNOWMAN_GAME
                    if prepositions_button.collidepoint(event.pos):
                        game_state = PREPOSITION_GAME
                    if vocabulary_button.collidepoint(event.pos):
                        game_state = VOCABULARY_GAME

        elif game_state == SNOWMAN_GAME:
            # Display the snowman screen
            back_button = snowman_levels_screen()

            # Event handling for the game screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        game_state = GAMES_BOARD_SCREEN

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
