import pygame
import sys
from snowman.constants import GAMES_BOARD_SCREEN, GAME_SCREEN_BG, screen, TITLE_HEIGHT, MENU_BUTTON_HEIGHT, \
    BUTTON_WIDTH, LONG_PADDING, SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BUTTON_WIDTH, SMALL_PADDING, MAIN_MENU, SNOWMAN_GAME, \
    PREPOSITION_GAME, VOCABULARY_GAME
from snowman.utility import draw_title, draw_subtitle, draw_button


pygame.init()


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
    back_button = draw_button("رجوع", 30, (TITLE_HEIGHT - MENU_BUTTON_HEIGHT) / 2, BUTTON_WIDTH - LONG_PADDING,
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
    draw_subtitle("أشكال المبتدأ", SCREEN_WIDTH - edge_space - 10, y_coordinate - 90, brown)

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
                               SCREEN_HEIGHT // 2 - MENU_BUTTON_HEIGHT - SMALL_PADDING, MENU_BUTTON_WIDTH,
                               MENU_BUTTON_HEIGHT)
    button_options = draw_button("الإعدادات", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                                 SCREEN_HEIGHT // 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
    button_quit = draw_button("الخروج", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                              SCREEN_HEIGHT // 2 + MENU_BUTTON_HEIGHT + SMALL_PADDING, MENU_BUTTON_WIDTH,
                              MENU_BUTTON_HEIGHT)

    return button_start, button_options, button_quit


# Main game loop
def main():
    global game_state
    game_state = MAIN_MENU  # Start with the menu screen
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill("black")  # Set background color of the screen

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
