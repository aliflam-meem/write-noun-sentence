import sys

import pygame

from src.constants import screen, GAME_SCREEN_BG, SCREEN_WIDTH, BUTTON_WIDTH, BUTTON_HEIGHT, SCREEN_HEIGHT, \
    MENU_BUTTON_WIDTH, SMALL_PADDING, MAIN_MENU, GAMES_BOARD_SCREEN, \
    WHACK_A_MOLE_GAME, JAR_BINGO_GAME, SNOWMAN_LEVELS, SNOWMAN_GAME, gainsboro, GAME_SCREEN_SECONDARY_BG, \
    SNOWMAN_LOADING_SCREEN, maroon
from src.core.audio_player import play_background_sound, pause_background_sound
from src.core.utility import draw_title, draw_back_button, draw_button, load_loading_image
from src.jar_bingo.constants import BACKGROUND_SEA_SHP
from src.jar_bingo.game import JBGameComponents
from src.jar_bingo.game_utils import load_jar_bingo_game_thumbnail
from src.snowman.constants import snowman_levels_keys, snowman_levels
from src.snowman.game import SnowmanGame
from src.snowman.scences import create_input_box, snowman_levels_screen, snowman_game_screen, \
    load_snowman_game_thumbnail, snowman_loading_game_screen
from src.whack_a_mole.constants import WM_MUSIC
from src.whack_a_mole.game import WhackaMoleGame
from src.whack_a_mole.game import whack_a_mole_game_screen, load_mole_game_thumbnail, display_game_result


def quit_game():
    pygame.quit()
    sys.exit()


# Function to handle the game screen
def games_board_screen():
    # Draw background and title
    screen.blit(GAME_SCREEN_SECONDARY_BG, (0, 0))
    draw_title("قائمة الألعاب")

    # Draw a "Back to Menu" button
    back_button = draw_back_button()

    # Button layout parameters
    space_between_buttons = 20  # space between buttons
    edge_space = (SCREEN_WIDTH - (
        BUTTON_WIDTH * 3 + space_between_buttons * 2)) / 2  # space between screen edges and buttons
    y_coordinate = SCREEN_HEIGHT // 2 + BUTTON_HEIGHT  # y-coordinate for buttons

    # x-coordinates based on edge_space and space_between_buttons
    vocabulary_button_x = SCREEN_WIDTH - edge_space - BUTTON_WIDTH
    prepositions_button_x = vocabulary_button_x - BUTTON_WIDTH - space_between_buttons
    snowman_button_x = prepositions_button_x - BUTTON_WIDTH - space_between_buttons

    # Load images
    whack_a_mole_thumbnail = load_mole_game_thumbnail()
    jar_bingo_thumbnail = load_jar_bingo_game_thumbnail()
    snowman_thumbnail = load_snowman_game_thumbnail()

    # Border settings
    border_thickness = 4
    border_radius = 10  # Adjust for rounded corners
    border_color = gainsboro

    # Function to create a bordered, rounded-corner surface
    def create_bordered_image(image):
        # Create a surface with border
        border_surface = pygame.Surface((image.get_width() + 2 * border_thickness,
                                         image.get_height() + 2 * border_thickness), pygame.SRCALPHA)

        # Draw rounded rectangle on the border surface
        pygame.draw.rect(border_surface, border_color, border_surface.get_rect(), border_radius=border_radius)

        # Blit the original image onto the center of the border surface
        border_surface.blit(image, (border_thickness, border_thickness))

        return border_surface

    # Create bordered images
    whack_a_mole_thumbnail = create_bordered_image(whack_a_mole_thumbnail)
    jar_bingo_thumbnail = create_bordered_image(jar_bingo_thumbnail)
    snowman_thumbnail = create_bordered_image(snowman_thumbnail)

    # Define the y-coordinate offset for images
    thumbnail_y_offset = y_coordinate - whack_a_mole_thumbnail.get_height() - 10  # 10px above the button

    # Center each thumbnail above the button by aligning their centers
    screen.blit(whack_a_mole_thumbnail,
                (vocabulary_button_x + BUTTON_WIDTH // 2 - whack_a_mole_thumbnail.get_width() // 2, thumbnail_y_offset))
    screen.blit(jar_bingo_thumbnail,
                (prepositions_button_x + BUTTON_WIDTH // 2 - jar_bingo_thumbnail.get_width() // 2, thumbnail_y_offset))
    screen.blit(snowman_thumbnail,
                (snowman_button_x + BUTTON_WIDTH // 2 - snowman_thumbnail.get_width() // 2, thumbnail_y_offset))

    # Draw the buttons
    whack_a_mole_button = draw_button("إصابة القنفذ", vocabulary_button_x, y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)
    jar_bingo_button = draw_button("بينغو أحرف الجر", prepositions_button_x, y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)
    snowman_button = draw_button("الرجل الثلجي", snowman_button_x, y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)

    return back_button, whack_a_mole_button, jar_bingo_button, snowman_button


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
    show_snowman_loading_screen = True
    answer_box = create_input_box()
    clock = pygame.time.Clock()
    running = True
    snowman_current_game = SnowmanGame()
    whack_a_mole_game = WhackaMoleGame()
    #jar_bingo_game
    jar_bingo_game = JBGameComponents()
    play_background_sound(BACKGROUND_SEA_SHP, volume=0.5)
    pause_background_sound(True)
    bingo_bg_sound_state = True
    jar_bingo_initial = True
    # -----------------
    # screen.fill("black")  # Set background color of the screen (blocks my screen for some reason?So I moved it outside the while so it doesn't get displayed each time)

    play_background_sound(WM_MUSIC, volume=0.5)
    pause_background_sound(True)
    while running:

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
            back_button, whack_a_mole_button, jarbingo_button, snowman_button = games_board_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        game_state = MAIN_MENU
                    if snowman_button.collidepoint(event.pos):
                        game_state = SNOWMAN_LEVELS
                    if jarbingo_button.collidepoint(event.pos):
                        game_state = JAR_BINGO_GAME
                        jar_bingo_game.restart_game(jar_bingo_initial)
                        bingo_bg_sound_state = True
                        if jar_bingo_initial == True:
                            jar_bingo_initial = False
                    if whack_a_mole_button.collidepoint(event.pos):
                        game_state = WHACK_A_MOLE_GAME
                        whack_a_mole_game.reset_game()

        elif game_state == SNOWMAN_LEVELS:
            back_button, al_atareef_button, demonstratives_button, pronouns_button, sound_button = snowman_levels_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        game_state = GAMES_BOARD_SCREEN
                    if sound_button.collidepoint(event.pos):
                        pause_background_sound(snowman_current_game.is_sound_on)
                        snowman_current_game.is_sound_on = not snowman_current_game.is_sound_on
                    if al_atareef_button.collidepoint(event.pos):
                        game_state = SNOWMAN_LOADING_SCREEN
                        show_snowman_loading_screen = True
                        snowman_current_game.questions_count_per_type = 2
                        snowman_current_game.level = snowman_levels_keys[0]
                        answer_box.clear()
                    if demonstratives_button.collidepoint(event.pos):
                        game_state = SNOWMAN_LOADING_SCREEN
                        show_snowman_loading_screen = True
                        snowman_current_game.questions_count_per_type = 10
                        snowman_current_game.level = snowman_levels_keys[1]
                        answer_box.clear()
                    if pronouns_button.collidepoint(event.pos):
                        game_state = SNOWMAN_LOADING_SCREEN
                        show_snowman_loading_screen = True
                        snowman_current_game.questions_count_per_type = 3
                        snowman_current_game.level = snowman_levels_keys[2]
                        answer_box.clear()
        elif game_state == SNOWMAN_LOADING_SCREEN:
            pause_background_sound(False)
            title = snowman_levels[snowman_levels_keys[1]]["title"]
            if snowman_current_game.get_current_question() == "" and show_snowman_loading_screen:
                show_snowman_loading_screen = False
                snowman_loading_game_screen(title)
                load_loading_image(text_color=maroon)
                snowman_current_game.reset_game()
            elif snowman_current_game.get_current_question() != "":
                game_state = SNOWMAN_GAME
        elif game_state == SNOWMAN_GAME:
            print(len(snowman_current_game.questions))
            title = snowman_levels[snowman_current_game.level]["title"]
            stop_game_interaction = snowman_current_game.is_win is not None
            back_button, buttons, submit_answer_button, sound_button = snowman_game_screen(answer_box,
                                                                                           snowman_current_game.get_current_question(),
                                                                                           title,
                                                                                           snowman_current_game.score,
                                                                                           snowman_current_game.health_points,
                                                                                           snowman_current_game.get_current_melting_snowman_image(),
                                                                                           snowman_current_game.get_current_information(),
                                                                                           snowman_current_game.can_submit_answer(),
                                                                                           snowman_current_game.can_proceed_to_next_question(),
                                                                                           snowman_current_game.is_user_answer_correct)
            correct_button, help_button, grammar_button, next_question_button = buttons

            # Automatically advance if we are waiting and a new question becomes available
            # print("questions) > snowman_current_game.question_index + 1 ",
            #       snowman_current_game.waiting_for_next_question \
            #       and len(snowman_current_game.questions) > snowman_current_game.question_index + 1)
            if snowman_current_game.waiting_for_next_question \
                and len(snowman_current_game.questions) > snowman_current_game.question_index + 1 \
                and not snowman_current_game.reached_last_question():
                # Move to the next question
                answer_box.clear()
                snowman_current_game.move_to_next_question()

            # If max questions are reached, disable waiting for next question
            # print("len(snowman_current_game.questions) == snowman_current_game.total_questions_count ",
            #       len(snowman_current_game.questions) == snowman_current_game.total_questions_count)
            if len(snowman_current_game.questions) == snowman_current_game.total_questions_count:
                snowman_current_game.waiting_for_next_question = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        game_state = SNOWMAN_LEVELS
                        snowman_current_game.reset_questions_list()
                    if sound_button.collidepoint(event.pos):
                        pause_background_sound(snowman_current_game.is_sound_on)
                        snowman_current_game.is_sound_on = not snowman_current_game.is_sound_on
                    # Handle the game button if the game isn't over and the result screen isn't displayed yet
                    if not stop_game_interaction:
                        if next_question_button.collidepoint(event.pos) and not snowman_current_game.is_game_over():
                            # Move to the next question
                            answer_box.clear()
                            snowman_current_game.move_to_next_question()
                        if submit_answer_button.collidepoint(event.pos):
                            if not snowman_current_game.is_correct_answer_displayed or \
                                (
                                    snowman_current_game.is_correct_answer_displayed and snowman_current_game.reached_last_question()):
                                if snowman_current_game.is_answer_valid(answer_box):
                                    if snowman_current_game.reached_last_question():
                                        pause_background_sound(True)
                                        snowman_current_game.is_sound_on = False
                                        # We've reached the last question already --> show final score and result
                                        snowman_current_game.finalize_game()
                                        snowman_current_game.display_result_and_play_sound()
                                    else:
                                        snowman_current_game.is_user_answer_correct = True
                                else:
                                    if snowman_current_game.health_points > 0:
                                        snowman_current_game.health_points -= 1
                                    elif snowman_current_game.health_points == 0:
                                        snowman_current_game.increase_wrong_answers()
                                        snowman_current_game.move_to_next_snowman_melting_image()
                                        if snowman_current_game.are_all_answers_wrong():
                                            pause_background_sound(True)
                                            snowman_current_game.is_sound_on = False
                                            # We've reached the last question already or the snowman has melted --> show
                                            # final score and result
                                            snowman_current_game.finalize_game()
                                            snowman_current_game.display_result_and_play_sound()

                        if correct_button.collidepoint(event.pos):
                            snowman_current_game.set_correct_answer_as_information()
                        if help_button.collidepoint(event.pos):
                            snowman_current_game.set_help_questions_as_information()
                        if grammar_button.collidepoint(event.pos):
                            snowman_current_game.set_grammar_as_information()

                answer_box.handle_event(event)
            answer_box.draw()
            # Display the spinner only if waiting_for_next_question is True and we haven't reached max questions
            if snowman_current_game.waiting_for_next_question:
                load_loading_image(text_message="", text_color=maroon)
            if snowman_current_game.is_win is not None:
                pause_background_sound(True)
                snowman_current_game.is_sound_on = False
                snowman_current_game.display_result_and_play_sound()

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

            if whack_a_mole_game.game_over:
                pause_background_sound(True)
                display_game_result(whack_a_mole_game)

            if whack_a_mole_game.game_end:
                pause_background_sound(True)
                display_game_result(whack_a_mole_game)


            if whack_a_mole_game.lives <= 0:
                whack_a_mole_game.game_over = True


            if not whack_a_mole_game.game_over and not whack_a_mole_game.game_end:
                whack_a_mole_game.show_up_timer += 2
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

            if game_state != WHACK_A_MOLE_GAME:
                pause_background_sound(True)

        elif game_state == JAR_BINGO_GAME:
            if bingo_bg_sound_state:#resume the bg sound.
                pause_background_sound(False)
            running, game_state, bingo_bg_sound_state  = jar_bingo_game.play_jar_bingo_game(running, back_button, JAR_BINGO_GAME)
            if game_state != JAR_BINGO_GAME:
                pause_background_sound(True)

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
