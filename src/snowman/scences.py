from src.constants import SCREEN_WIDTH, IMAGE_WIDTH, SMALL_PADDING, BUTTON_WIDTH, LONG_PADDING, SMALL_BUTTON_HEIGHT, \
    SCREEN_HEIGHT, screen, BUTTON_HEIGHT, TITLE_HEIGHT, SCOREBAR_HEIGHT, thumbnail_width, BUTTON_COLOR
from src.core.input import InputBox
from src.core.utility import draw_title, draw_back_button, draw_subtitle, draw_button, draw_text_box, \
    draw_score_and_health, load_image, draw_sound_button
from src.snowman.constants import snowman_levels, SNOWMAN_GAME_SCREEN_BG, snowman_thumbnail, SNOWMAN_GAME_SCREEN_BG_TRA, \
    CHECK_MARK_IMAGE_PATH


def snowman_levels_screen():
    screen.blit(load_snowman_game_background(), (0, 0))
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
    sound_button = draw_sound_button()
    # 10 pixels is a magic number, right indent
    draw_subtitle("أشكال المبتدأ", SCREEN_WIDTH - edge_space - 10, y_coordinate - 90, BUTTON_COLOR)

    # Draw menu buttons
    al_atareef_button = draw_button(snowman_levels["al_atareef"]["title"], al_atareef_button_x,
                                    y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)
    demonstratives_button = draw_button(snowman_levels["demonstratives"]["title"], demonstratives_button_x,
                                        y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)
    pronouns_button = draw_button(snowman_levels["pronouns"]["title"], pronouns_button_x,
                                  y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)

    return back_button, al_atareef_button, demonstratives_button, pronouns_button, sound_button


def draw_question_interface(answer_box, question_text, snowman_image, is_submit_button_enabled, is_user_answer_correct):
    check_mark_image = load_image(CHECK_MARK_IMAGE_PATH, (30, 30))

    # Space between elements
    space_between_elements = 30

    question_box_width = SCREEN_WIDTH - IMAGE_WIDTH - SMALL_PADDING
    question_box_height = 130

    # Draw question text (right-aligned)
    question_text_x = IMAGE_WIDTH  # Aligned with buttons
    question_text_y = TITLE_HEIGHT + SMALL_PADDING  # Top quarter of the screen for question text
    draw_text_box(question_text, question_text_x, question_text_y, question_box_width, question_box_height)

    # Calculate positions for the buttons (right-aligned and horizontally aligned)
    answer_box_y = question_text_y + question_box_height + space_between_elements  # Below question text
    answer_box_x = question_text_x + BUTTON_WIDTH / 2 + SMALL_PADDING
    answer_box.set_rect_y(answer_box_y)
    answer_box.set_rect_x(answer_box_x)
    submit_answer_button_x = question_text_x  # Right-most button
    submit_answer_button = draw_button("أجب", submit_answer_button_x, answer_box_y, BUTTON_WIDTH / 2,
                                       SMALL_BUTTON_HEIGHT, is_disabled=not is_submit_button_enabled)

    # Draw check mark image if the answer is correct
    if is_user_answer_correct:
        check_mark_x = submit_answer_button_x - check_mark_image.get_width() - SMALL_PADDING  # Position to the left of the button
        check_mark_y = answer_box_y  # Align vertically with the button
        screen.blit(check_mark_image, (check_mark_x, check_mark_y))

    # Draw snowman image to the left of the buttons
    image_x = 0  # Image aligned to the left of screen
    image_y = question_text_y + SCOREBAR_HEIGHT  # Aligned vertically with the question text
    screen.blit(snowman_image, (image_x, image_y))

    # Return the interface elements (for any potential further processing)
    return {
        "submit_answer_button": submit_answer_button,
        "button_y": answer_box_y + answer_box.rect.height + space_between_elements,
        "information_area_x": answer_box_x
    }


def draw_helping_buttons(y, is_next_question_button_enabled):
    # Space between elements
    space_between_elements = 30

    # Calculate the right-most x-coordinate for alignment
    right_alignment_x = SCREEN_WIDTH - SMALL_PADDING

    # Draw buttons
    help_button_x = right_alignment_x - BUTTON_WIDTH  # Right-most button
    help_button = draw_button("الأسئلة المساعدة", help_button_x, y, BUTTON_WIDTH, SMALL_BUTTON_HEIGHT, True)
    correct_button_x = help_button.x - BUTTON_WIDTH - space_between_elements  # Middle button
    correct_button = draw_button("الإجابة الصحيحة", correct_button_x, y, BUTTON_WIDTH, SMALL_BUTTON_HEIGHT, True)
    grammar_button_x = correct_button.x - BUTTON_WIDTH - space_between_elements  # Left-most button
    grammar_button = draw_button("القاعدة", grammar_button_x, y, BUTTON_WIDTH, SMALL_BUTTON_HEIGHT, True)
    next_question_button_x = grammar_button.x - BUTTON_WIDTH - space_between_elements  # Left-most button
    next_question_button = draw_button("السؤال التالي", next_question_button_x, y, BUTTON_WIDTH,
                                       SMALL_BUTTON_HEIGHT, True, is_disabled=not is_next_question_button_enabled)

    return correct_button, help_button, grammar_button, next_question_button


def snowman_loading_game_screen(title):
    background = load_snowman_game_background(True)
    screen.blit(background, (0, 0))
    draw_title(title)
    back_button = draw_back_button()

    return back_button


def snowman_game_screen(answer_box, question, title, score, health_points, image,
                        information_area_content, is_submit_button_enabled,
                        is_next_question_button_enabled, is_user_answer_correct):
    back_button = snowman_loading_game_screen(title)
    sound_button = draw_sound_button()
    score_y = TITLE_HEIGHT + SMALL_PADDING
    draw_score_and_health(score, y=score_y, health_points=health_points)
    elements = draw_question_interface(answer_box, question, image, is_submit_button_enabled, is_user_answer_correct)
    buttons = draw_helping_buttons(elements["button_y"], is_next_question_button_enabled)
    information_area_y = SMALL_BUTTON_HEIGHT + elements["button_y"] + SMALL_PADDING
    draw_text_box(information_area_content, answer_box.rect.x, information_area_y, answer_box.rect.width,
                  answer_box.rect.height)

    return back_button, buttons, elements["submit_answer_button"], sound_button


def create_input_box():
    input_box_width = SCREEN_WIDTH - IMAGE_WIDTH - 2 * SMALL_PADDING - BUTTON_WIDTH / 2
    input_box_height = SMALL_BUTTON_HEIGHT
    # Draw input box below the buttons (right-aligned)
    input_box_y = SCREEN_HEIGHT - 2 * LONG_PADDING
    input_box_x = IMAGE_WIDTH + SMALL_PADDING

    # Create an instance of InputBox instead of using draw_input_box
    return InputBox(input_box_x, input_box_y, input_box_width, input_box_height)


def load_snowman_game_thumbnail():
    return load_image(snowman_thumbnail, (thumbnail_width, thumbnail_width))


def load_snowman_game_background(transparent=False):
    if transparent:
        return load_image(SNOWMAN_GAME_SCREEN_BG_TRA, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return load_image(SNOWMAN_GAME_SCREEN_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
