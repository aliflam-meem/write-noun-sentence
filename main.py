import sys

import pygame

from src.constants import screen, GAME_SCREEN_BG, SCREEN_WIDTH, BUTTON_WIDTH, BUTTON_HEIGHT, SCREEN_HEIGHT, \
    MENU_BUTTON_WIDTH, SMALL_PADDING, MAIN_MENU, GAMES_BOARD_SCREEN, \
    WHACK_A_MOLE_GAME, PREPOSITION_GAME, SNOWMAN_LEVELS, SNOWMAN_GAME
from src.core.utility import draw_title, draw_back_button, draw_button
from src.snowman.constants import snowman_levels_keys, snowman_levels
from src.snowman.game import SnowmanGame, validate_answer
from src.snowman.scences import create_input_box, snowman_levels_screen, snowman_game_screen
from src.whack_a_mole.game import whack_a_mole_game_screen,whack_a_mole_play_audio, WhackaMoleGame


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


# Main game loop
def main():
    global game_state
    game_state = MAIN_MENU  # Start with the menu screen
    answer_box = create_input_box()
    clock = pygame.time.Clock()
    running = True
    snowman_current_game = SnowmanGame()
    whack_a_mole_game = WhackaMoleGame()
    initialize_jarbingo_game_in_main()
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
            whack_a_mole_game = whack_a_mole_game_screen(whack_a_mole_game)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        game_state = GAMES_BOARD_SCREEN
                    mousePos = pygame.mouse.get_pos()
                    for mole in whack_a_mole_game.moles:
                        if mole.is_clicked(mousePos):
                            # if mole.is_correct_answer():
                            clicked_answer = mole.clicked_answer();
                            if clicked_answer == whack_a_mole_game.questions[whack_a_mole_game.current_question_index]["answer"]:
                                #print(clicked_answer)  # for debugging                
                                whack_a_mole_game.score += 1
                                mole.move = False
                                mole.counter = 0
                                whack_a_mole_game.current_question_index +=1
                                whack_a_mole_game.generate_new_gtts = True
                            else:
                                whack_a_mole_game.lives -= 1
                                mole.move = False
                                mole.counter = 0

                    if whack_a_mole_game.bomb.is_clicked(mousePos):
                        whack_a_mole_game.lives -= 1
                        whack_a_mole_game.bomb.move = False
                        whack_a_mole_game.bomb.counter = 0

            if whack_a_mole_game.lives <= 0:
                whack_a_mole_game.game_over = True

            #if whack_a_mole_game.game_end == True: 
                # turn off the game after 3 seconds
                #whack_a_mole_game.game_end_counter += 1
                #if whack_a_mole_game.game_end_counter >= 180:
                #    in_play = False

            if not whack_a_mole_game.game_over and not whack_a_mole_game.game_end:
                whack_a_mole_game.show_up_timer += 1
                if whack_a_mole_game.show_up_timer >= whack_a_mole_game.show_up_end:
                    # holes that are already taken
                    taken_holes = [mole.hole_num
                                    for mole in whack_a_mole_game.moles] + [whack_a_mole_game.bomb.hole_num]

                    # select a new hole for each mole
                    for mole in whack_a_mole_game.moles:
                        if not mole.move:
                            mole.select_hole(taken_holes)
                            taken_holes.append(mole.hole_num)
                            break

                    # select a new hole for the bomb
                    if not whack_a_mole_game.bomb.move:
                        whack_a_mole_game.bomb.select_hole(taken_holes)

                    whack_a_mole_game.show_up_timer = 0

                for mole in whack_a_mole_game.moles:
                    mole.show()
                whack_a_mole_game.bomb.show()

        elif game_state == JAR_BINGO_GAME:
            print_jarbingo_game_screen()

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
