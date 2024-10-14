import pygame
import sys


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
TITLE_HEIGHT = 100
IMAGE_WIDTH = 200
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 50
PADDING = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
BUTTON_COLOR = (70, 130, 180)
GAME_SCREEN_BG = pygame.image.load("main_bg.jpg")
GAME_SCREEN_BG = pygame.transform.scale(GAME_SCREEN_BG, (SCREEN_WIDTH,SCREEN_HEIGHT))

# Create the Pygame screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ألف لام ميم")

# Load fonts
title_font = pygame.font.Font("Arial.ttf", 48)
title_font.set_script("Arab")
title_font.set_direction(pygame.DIRECTION_RTL)
body_font = pygame.font.Font("Arial.ttf", 30)
body_font.set_script("Arab")
body_font.set_direction(pygame.DIRECTION_RTL)

# Load images (You would load your own image files here)
# For demonstration purposes, let's assume we have 5 images loaded
# Replace the "image_path" with actual image paths
images = [
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT/2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT/2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT/2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT/2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT/2))  # Placeholder surface as an image
]

# Game states
MENU = "menu"
GAME_SCREEN = "games_board_screen"


# Function to draw the title with background
def draw_title(title):
    title_background_rect = pygame.Rect(0, 0, SCREEN_WIDTH, TITLE_HEIGHT)
    pygame.draw.rect(screen, DARK_GRAY, title_background_rect)

    title_text = title_font.render(title, True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, TITLE_HEIGHT // 2))
    screen.blit(title_text, title_rect)


# Function to create buttons
def draw_button(text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, LIGHT_GRAY, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

    button_text = body_font.render(text, True, WHITE)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    return button_rect


# Dummy action to switch to a new screen (the game screen)
def start_game():
    global game_state
    print("Switching to the game screen...")
    game_state = GAME_SCREEN


# Action to quit the game
def quit_game():
    print("Quitting the game...")
    pygame.quit()
    sys.exit()


# Function to handle the game screen
def games_board_screen():
    # Fill the screen with a different background
    # screen.fill(GAME_SCREEN_BG)
    # img_surface.blit(image, (0, 0))
    # window.blit(img_surface, (0, 0))
    screen.blit(GAME_SCREEN_BG, (0, 0))
    draw_title("قائمة الألعاب")

    # Draw a "Back to Menu" button
    button_back = draw_button("رجوع", 30,(TITLE_HEIGHT-MENU_BUTTON_HEIGHT)/2, MENU_BUTTON_WIDTH - PADDING, MENU_BUTTON_HEIGHT)

    # List the games buttons
    space_between_buttons = 20  # space between buttons
    edge_space = 30  # space between screen edges and buttons

    # y-coordinate is the same for all buttons, vertically centered
    y_coordinate = SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT // 2

    # x-coordinates based on edge_space and space_between_buttons
    vocabulary_button_x = edge_space
    prepositions_button_x = vocabulary_button_x + MENU_BUTTON_WIDTH + space_between_buttons
    snowman_button_x = prepositions_button_x + MENU_BUTTON_WIDTH + space_between_buttons

    # Draw buttons
    vocabulary_button = draw_button("إصابة القنفذ", vocabulary_button_x, y_coordinate, MENU_BUTTON_WIDTH,
                                    MENU_BUTTON_HEIGHT)
    prepositions_button = draw_button("بينغو", prepositions_button_x, y_coordinate, MENU_BUTTON_WIDTH,
                                      MENU_BUTTON_HEIGHT)
    snowman_button = draw_button("الرجل الثلجي", snowman_button_x, y_coordinate, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)

    return button_back, vocabulary_button, prepositions_button, snowman_button


# Main game loop
def main():
    global game_state
    game_state = MENU  # Start with the menu screen
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)  # Set background color of the screen

        # Handle different screens based on game state
        if game_state == MENU:
            draw_title("ألف لام ميم")

            # Draw menu buttons
            button_start = draw_button("الألعاب", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                                       SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
            button_options = draw_button("الإعدادات", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                                         SCREEN_HEIGHT // 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
            button_quit = draw_button("الخروج", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                                      SCREEN_HEIGHT // 2 + MENU_BUTTON_HEIGHT, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)

            # Event handling for menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    if button_start.collidepoint(event.pos):
                        start_game()  # Switch to game screen
                    elif button_options.collidepoint(event.pos):
                        print("Options button clicked (dummy action)")
                    elif button_quit.collidepoint(event.pos):
                        quit_game()

        elif game_state == GAME_SCREEN:
            # Display the game screen
            button_back,vocabulary_button, prepositions_button, snowman_button  = games_board_screen()

            # Event handling for the game screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    if button_back.collidepoint(event.pos):
                        print("Back to Menu button clicked")
                        game_state = MENU  # Switch back to the menu

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
