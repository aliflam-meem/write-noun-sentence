import sys

from constants import *
from core.input import InputBox
from core.utility import draw_title, draw_button, draw_back_button
from snowman.constants import snowman_levels, snowman_levels_keys
from snowman.game import validate_answer, SnowmanGame
from snowman.scences import snowman_levels_screen, snowman_game_screen
from whack_a_mole.game import whack_a_mole_game_screen


def quit_game():
    pygame.quit()
    sys.exit()


# Function to handle the game screen
def games_board_screen():
    screen.blit(GAME_SCREEN_BG, (0, 0))
    draw_title("قائمة الألعاب")

    # Draw a "Back to Menu" button
    back_button = draw_back_button()

    # List the games buttons
    space_between_buttons = 20  # space between buttons
    edge_space = (SCREEN_WIDTH - (
        BUTTON_WIDTH * 3 + space_between_buttons * 2)) / 2  # space between screen edges and buttons

    # y-coordinate is the same for all buttons, vertically centered
    y_coordinate = SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2

    # x-coordinates based on edge_space and space_between_buttons
    vocabulary_button_x = SCREEN_WIDTH - edge_space - BUTTON_WIDTH
    prepositions_button_x = vocabulary_button_x - BUTTON_WIDTH - space_between_buttons
    snowman_button_x = prepositions_button_x - BUTTON_WIDTH - space_between_buttons

    # Draw buttons
    whack_a_mole_button = draw_button("إصابة القنفذ", vocabulary_button_x, y_coordinate, BUTTON_WIDTH,
                                      BUTTON_HEIGHT)
    prepositions_button = draw_button("بينغو", prepositions_button_x, y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)
    snowman_button = draw_button("الرجل الثلجي", snowman_button_x, y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)

    return back_button, whack_a_mole_button, prepositions_button, snowman_button


def main_menu_screen():
    screen.blit(GAME_SCREEN_BG, (0, 0))
    draw_title("ألف لام ميم")

    # Draw menu buttons
    button_start = draw_button("الألعاب", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                               SCREEN_HEIGHT // 2 - BUTTON_HEIGHT - SMALL_PADDING, MENU_BUTTON_WIDTH,
                               BUTTON_HEIGHT)
    button_options = draw_button("الإعدادات", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                                 SCREEN_HEIGHT // 2, MENU_BUTTON_WIDTH, BUTTON_HEIGHT)
    button_quit = draw_button("الخروج", SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2,
                              SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + SMALL_PADDING, MENU_BUTTON_WIDTH,
                              BUTTON_HEIGHT)

    return button_start, button_options, button_quit


def create_input_box():
    input_box_width = SCREEN_WIDTH - IMAGE_WIDTH - 2 * SMALL_PADDING - BUTTON_WIDTH / 2
    input_box_height = SMALL_BUTTON_HEIGHT
    # Draw input box below the buttons (right-aligned)
    input_box_y = SCREEN_HEIGHT - 2 * LONG_PADDING
    input_box_x = IMAGE_WIDTH + SMALL_PADDING

    # Create an instance of InputBox instead of using draw_input_box
    return InputBox(input_box_x, input_box_y, input_box_width, input_box_height)


# Main game loop
def main():
    global game_state
    game_state = MAIN_MENU  # Start with the menu screen
    answer_box = create_input_box()
    clock = pygame.time.Clock()
    running = True
    snowman_current_game = SnowmanGame()

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
                        game_state = GAMES_BOARD_SCREEN
                    elif button_options.collidepoint(event.pos):
                        pass
                    elif button_quit.collidepoint(event.pos):
                        quit_game()

        elif game_state == GAMES_BOARD_SCREEN:
            back_button, whack_a_mole_button, prepositions_button, snowman_button = games_board_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        game_state = MAIN_MENU
                    if snowman_button.collidepoint(event.pos):
                        game_state = SNOWMAN_LEVELS
                    if prepositions_button.collidepoint(event.pos):
                        game_state = PREPOSITION_GAME
                    if whack_a_mole_button.collidepoint(event.pos):
                        game_state = WHACK_A_MOLE_GAME

        elif game_state == SNOWMAN_LEVELS:
            back_button, al_atareef_button, demonstratives_button, pronouns_button = snowman_levels_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        game_state = GAMES_BOARD_SCREEN
                    if back_button.collidepoint(event.pos):
                        game_state = MAIN_MENU
                    if al_atareef_button.collidepoint(event.pos):
                        game_state = SNOWMAN_GAME
                        snowman_current_game.level = snowman_levels_keys[0]
                        snowman_current_game.questions_count_per_type = 2
                        snowman_current_game.reset_game()
                        snowman_current_game.initialize_game()
                    if demonstratives_button.collidepoint(event.pos):
                        game_state = SNOWMAN_GAME
                        snowman_current_game.level = snowman_levels_keys[1]
                        snowman_current_game.questions_count_per_type = 10
                        snowman_current_game.reset_game()
                        snowman_current_game.initialize_game()
                    if pronouns_button.collidepoint(event.pos):
                        game_state = SNOWMAN_GAME
                        snowman_current_game.level = snowman_levels_keys[2]
                        snowman_current_game.questions_count_per_type = 3
                        snowman_current_game.reset_game()
                        snowman_current_game.initialize_game()

        elif game_state == SNOWMAN_GAME:
            title = snowman_levels[snowman_current_game.level]["title"]
            back_button, buttons = snowman_game_screen(answer_box,
                                                       snowman_current_game.get_current_question(), title,
                                                       snowman_current_game.score,
                                                       snowman_current_game.health_points,
                                                       snowman_current_game.get_current_melting_snowman_image())
            correct_button, help_button, grammar_button = buttons

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        game_state = SNOWMAN_LEVELS
                    if correct_button.collidepoint(event.pos):
                        if validate_answer(snowman_current_game, answer_box):
                            if snowman_current_game.reached_last_question():
                                # We've reached the last question already --> show final score and result
                                snowman_current_game.is_win = True
                                snowman_current_game.display_game_result()
                            else:
                                # Move to the next question
                                snowman_current_game.move_to_next_question()
                        else:
                            is_game_over = snowman_current_game.is_game_over()
                            if snowman_current_game.health_points > 0:
                                snowman_current_game.health_points -= 1
                            elif snowman_current_game.health_points == 0:
                                if is_game_over:
                                    # We've reached the last question already --> show final score and result
                                    # or the snowman is melted
                                    snowman_current_game.is_win = False
                                    snowman_current_game.display_game_result()
                                elif snowman_current_game.reached_last_question() and not is_game_over:
                                    # Move to the next question
                                    snowman_current_game.move_to_next_question()
                answer_box.handle_event(event)
            answer_box.draw()

        elif game_state == WHACK_A_MOLE_GAME:
            whack_a_mole_game_screen()

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
