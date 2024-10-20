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
                                        y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)
    pronouns_button = draw_button(snowman_levels["pronouns"]["title"], pronouns_button_x,
                                  y_coordinate, BUTTON_WIDTH, BUTTON_HEIGHT)

    return back_button, al_atareef_button, demonstratives_button, pronouns_button


def draw_question_interface(answer_box, question_text, snowman_image):
    # Space between elements
    space_between_elements = 20

    question_box_width = SCREEN_WIDTH - IMAGE_WIDTH - SMALL_PADDING
    question_box_height = 130

    # Draw question text (right-aligned)
    question_text_x = IMAGE_WIDTH  # Aligned with buttons
    question_text_y = TITLE_HEIGHT + SMALL_PADDING  # Top quarter of the screen for question text
    draw_text_box(question_text, question_text_x, question_text_y, question_box_width,
                  question_box_height)

    # Calculate positions for the buttons (right-aligned and horizontally aligned)
    answer_box_y = question_text_y + question_box_height + space_between_elements  # Below question text
    answer_box.set_rect_y(answer_box_y)
    answer_box.set_rect_x(question_text_x + BUTTON_WIDTH / 2 + SMALL_PADDING)
    answer_button_x = question_text_x  # Right-most button
    answer_button = draw_button("أجب", answer_button_x, answer_box_y, BUTTON_WIDTH / 2, SMALL_BUTTON_HEIGHT)

    # Draw image to the left of the buttons
    image_x = 0  # Image aligned to the left of screen
    image_y = question_text_y + SCOREBAR_HEIGHT  # Aligned vertically with the question text

    screen.blit(snowman_image, image_x, image_y)

    # Return the interface elements (for any potential further processing)
    return {
        "answer_button": answer_button,
        "button_y": answer_box_y + answer_box.rect.height + space_between_elements,
    }


def draw_helping_buttons(y):
    # Space between elements
    space_between_elements = 20

    # Calculate the right-most x-coordinate for alignment
    right_alignment_x = SCREEN_WIDTH - SMALL_PADDING

    # Draw buttons
    help_button_x = right_alignment_x - BUTTON_WIDTH  # Right-most button
    help_button = draw_button("الأسئلة المساعدة", help_button_x, y, BUTTON_WIDTH, SMALL_BUTTON_HEIGHT, True)
    correct_button_x = help_button.x - BUTTON_WIDTH - space_between_elements  # Middle button
    correct_button = draw_button("الإجابة الصحيحة", correct_button_x, y, BUTTON_WIDTH, SMALL_BUTTON_HEIGHT, True)
    grammar_button_x = correct_button.x - BUTTON_WIDTH - space_between_elements  # Left-most button
    grammar_button = draw_button("القاعدة", grammar_button_x, y, BUTTON_WIDTH, SMALL_BUTTON_HEIGHT, True)

    return correct_button, help_button, grammar_button


def snowman_game_screen(answer_box, question, title, score, health_points, image_path):
    screen.fill(cornsilk)
    draw_title(title)
    back_button = draw_back_button()
    score_y = TITLE_HEIGHT + SMALL_PADDING
    draw_score_and_health(score, y=score_y, health_points=health_points)
    elements = draw_question_interface(answer_box, question, image_path)
    buttons = draw_helping_buttons(elements["button_y"])

    return back_button, buttons
