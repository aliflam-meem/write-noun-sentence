import pygame
import sys


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define button dimensions
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 50

# Define game states
MENU = 0
GAME_SCREEN = 1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")

# Load fonts (replace with your desired font file)
font = body_font = pygame.font.Font("../snowman/Arial.ttf", 30)
font.set_script("Arab")
font.set_direction(pygame.DIRECTION_RTL)


# Function to draw a button
def draw_button(text, x, y, width, height, color=GRAY, text_color=WHITE):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)


# Function to draw the title
def draw_title():
    title_text = font.render("My Game", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)


# Function to draw the game screen (placeholder)
def game_screen():
    # Draw game elements here
    button_back = draw_button("Back", 50, 50, 150, 50)
    return button_back


# Function to start the game (placeholder)
def start_game():
    global game_state
    game_state = GAME_SCREEN


# Function to quit the game
def quit_game():
    pygame.quit()
    sys.exit()


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
            draw_title()

            # Draw menu buttons
            button_start = draw_button("Start", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                                       SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
            button_options = draw_button("Options", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                                         SCREEN_HEIGHT // 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
            button_quit = draw_button("Quit", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
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
            button_back = game_screen()

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
