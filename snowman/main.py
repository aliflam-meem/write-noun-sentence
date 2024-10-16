import pygame
import sys
from constants import *
from input import InputBox
from utility import draw_title, draw_subtitle, draw_button, draw_back_button, draw_image, draw_text_box


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
    vocabulary_button = draw_button("إصابة القنفذ", vocabulary_button_x, y_coordinate, BUTTON_WIDTH,
                                    BUTTON_HEIGHT)
    prepositions_button = draw_button("بينغو", prepositions_button_x, y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)
    snowman_button = draw_button("الرجل الثلجي", snowman_button_x, y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)

    return back_button, vocabulary_button, prepositions_button, snowman_button


def snowman_levels_screen():
    screen.blit(GAME_SCREEN_BG, (0, 0))
    draw_title("لعبة الرجل الثلجي")

    # List the games buttons
    space_between_buttons = 20  # space between buttons
    edge_space = (SCREEN_WIDTH - (
        BUTTON_WIDTH * 3 + space_between_buttons * 2)) / 2  # space between screen edges and buttons

    # y-coordinate is the same for all buttons, vertically centered
    y_coordinate = SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2

    # x-coordinates based on edge_space and space_between_buttons
    al_atareef_button_x = SCREEN_WIDTH - edge_space - BUTTON_WIDTH
    demonstratives_button_x = al_atareef_button_x - BUTTON_WIDTH - space_between_buttons
    pronouns_button_x = demonstratives_button_x - BUTTON_WIDTH - space_between_buttons

    back_button = draw_back_button()
    # 10 pixels is a magic number, right indent
    draw_subtitle("أشكال المبتدأ", SCREEN_WIDTH - edge_space - 10, y_coordinate - 90, brown)

    # Draw menu buttons
    al_atareef_button = draw_button(snowman_levels["al_atareef"]["title"], al_atareef_button_x,
                                    y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)
    demonstratives_button = draw_button(snowman_levels["demonstratives"]["title"], demonstratives_button_x,
                                        y_coordinate, BUTTON_WIDTH,BUTTON_HEIGHT)
    pronouns_button = draw_button(snowman_levels["pronouns"]["title"], pronouns_button_x,
                                  y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)

    return back_button, al_atareef_button, demonstratives_button, pronouns_button


def draw_question_interface(question_text, image_path, image_width=IMAGE_WIDTH, image_height=IMAGE_WIDTH):
    # Space between elements
    space_between_elements = 20

    question_box_width = SCREEN_WIDTH - image_width - SMALL_PADDING
    question_box_height = 300

    # Calculate the right-most x-coordinate for alignment
    right_alignment_x = SCREEN_WIDTH - SMALL_PADDING

    # Draw question text (right-aligned)
    question_text_x = image_width  # Aligned with buttons
    question_text_y = TITLE_HEIGHT + SMALL_PADDING  # Top quarter of the screen for question text
    draw_text_box(question_text, question_text_x, question_text_y,question_box_width, question_box_height )

    # Calculate positions for the buttons (right-aligned and horizontally aligned)
    button_y = question_text_y + question_box_height + space_between_elements # Below question text
    answer_button_x = right_alignment_x - BUTTON_WIDTH  # Right-most button
    help_button_x = answer_button_x - BUTTON_WIDTH - space_between_elements  # Middle button
    correct_button_x = help_button_x - BUTTON_WIDTH - space_between_elements  # Left-most button

    # Draw buttons
    correct_button = draw_button("الإجابة الصحيحة", correct_button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    help_button = draw_button("الأسئلة المساعدة", help_button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    answer_button = draw_button("أجب", answer_button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Draw image to the left of the buttons
    image_x = correct_button_x - image_width - space_between_elements  # Image aligned to the left of buttons
    image_y = question_text_y  # Aligned vertically with the question text
    draw_image(image_path, image_x, image_y, image_width, image_height)

    # Return the interface elements (for any potential further processing)
    return {
        "question_text": (question_text_x, question_text_y),
        "correct_button": correct_button,
        "help_button": help_button,
        "answer_button": answer_button,
        "image": (image_x, image_y),
        "input_box_y": button_y + BUTTON_HEIGHT + space_between_elements,
        "answer_box_x": question_text_x
    }


def snowman_game_screen(level=snowman_levels["pronouns"]["name"]):
    screen.fill(cornsilk)
    draw_title(snowman_levels[level]["title"])
    back_button = draw_back_button()
    question_text = "... من أهم مصادر الطاقة المتجددة."
    elements = draw_question_interface(question_text, "assets/complete.png")
    # handle_elements_actions(elements)

    return back_button, elements["input_box_y"], elements["answer_box_x"]


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
    input_box_width = SCREEN_WIDTH - IMAGE_WIDTH
    input_box_height = 60
    # Draw input box below the buttons (right-aligned)
    input_box_y = SCREEN_HEIGHT - 2*LONG_PADDING
    input_box_x = IMAGE_WIDTH + SMALL_PADDING

    # Create an instance of InputBox instead of using draw_input_box
    return InputBox(input_box_x, input_box_y, input_box_width, input_box_height)

# Main game loop
def main():
    global game_state
    game_state = MAIN_MENU  # Start with the menu screen
    snowman_level = snowman_levels["pronouns"]["name"]
    answer_box = create_input_box()
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
                        game_state = GAMES_BOARD_SCREEN
                    elif button_options.collidepoint(event.pos):
                        pass
                    elif button_quit.collidepoint(event.pos):
                        quit_game()

        elif game_state == GAMES_BOARD_SCREEN:
            back_button, vocabulary_button, prepositions_button, snowman_button = games_board_screen()

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
                    if vocabulary_button.collidepoint(event.pos):
                        game_state = VOCABULARY_GAME

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
                        snowman_level = snowman_levels["al_atareef"]["name"]
                    if demonstratives_button.collidepoint(event.pos):
                        game_state = SNOWMAN_GAME
                        snowman_level = snowman_levels["demonstratives"]["name"]
                    if pronouns_button.collidepoint(event.pos):
                        game_state = SNOWMAN_GAME
                        snowman_level = snowman_levels["pronouns"]["name"]
        elif game_state == SNOWMAN_GAME:
            back_button, answer_box_y, answer_box_x = snowman_game_screen(snowman_level)
            answer_box.y(answer_box_y)
            answer_box.x(answer_box_x)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        game_state = SNOWMAN_LEVELS
                answer_box.handle_event(event)
            answer_box.draw()

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
