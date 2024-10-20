import re
import sys

from constants import *
from input import InputBox
from learning_arabic_games.snowman.snowman_llm import load_game_data
from utility import draw_title, draw_subtitle, draw_button, draw_back_button, draw_text_box, \
    draw_score_and_health, format_questions_count_string


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


class SnowmanGame:

    def __init__(self, level=snowman_levels_keys[2], questions_count=1):
        self.isWin = None
        self.points_per_questions = 10
        self.melting_snowman_images = []
        self.melting_image_index = 0
        self.questions = []
        self.question_index = 0
        self.score = 0
        self.health_points = 2
        self.opened_help_questions = 0
        self.num_of_wrong_answers = 0
        self.level = level
        self.questions_count_per_type = questions_count
        self.max_questions_count_per_type = 5
        self.load_melting_snowman_images()

    def reset_game(self):
        self.isWin = None
        self.question_index = 0
        self.score = 0
        self.health_points = 2
        self.opened_help_questions = 0
        self.num_of_wrong_answers = 0
        self.melting_image_index = 0
        self.questions = []

    def generate_questions_data(self, noun_type):
        # Initialize the list to store all questions
        questions = []

        # Process the questions in chunks of 5
        total_questions_count = self.questions_count_per_type

        # Generate questions in batches of 5 until we run out of questions
        for i in range(0, total_questions_count, self.max_questions_count_per_type):
            # Determine how many questions to generate in the current batch
            questions_to_generate = min(self.max_questions_count_per_type, total_questions_count - i)

            # Format the questions count string (assuming it's for UI or logging)
            format_questions_count_string(questions_to_generate)

            # Load the question data for the current batch
            questions_data = load_game_data(noun_type, questions_to_generate)
            print(questions_data)
            # Process each question in the batch
            for question_dict in questions_data:
                question = question_dict["question"]
                # Replace any series of periods (e.g., ...) with '-------'
                question = re.sub(r'\.+', "-------", question)

                # Determine the number of words in the correct answer
                num_of_answer_words = len(question_dict["correct_answer"].split())

                # Determine the word description in Arabic
                if num_of_answer_words == 1:
                    num_words = "كلمة واحدة"
                elif num_of_answer_words == 2:
                    num_words = "كلمتين"
                else:
                    num_words = "أكثر من كلمتين"

                # Format the question with the correct word description
                question = f"املأ الفراغ التالي ب{num_words} بالمبتدأ المناسب.\n{question}"

                # Update the question in the dictionary
                question_dict["question"] = question

            # Add the processed questions to the final list
            questions.extend(questions_data)
        return questions


    def initialize_game(self):
        for n_type in snowman_levels[self.level]["noun_types"]:
            self.questions.extend(self.generate_questions_data(n_type))

    def load_melting_snowman_images(self):
        img = pygame.image.load("assets/complete.png")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load("assets/melting_1.png")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load("assets/melting_2.png")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load("assets/melting_3.png")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load("assets/melting_4.png")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load("assets/melted.jpg")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)


    def get_current_question(self):
        return self.questions[self.question_index]["question"]

    def get_current_correct_answer(self):
        return self.questions[self.question_index]["correct_answer"]

    def get_current_melting_snowman_image(self):
        return self.melting_snowman_images[self.melting_image_index]

    def is_game_over(self):
        return self.num_of_wrong_answers == len(self.melting_snowman_images) - 1 or self.reached_last_question()

    def reached_last_question(self):
        return self.question_index == len(self.questions) - 1

    def move_to_next_snowman_melting_image(self):
        self.melting_image_index += 1

    def move_to_next_question(self):
        self.question_index += 1
        self.move_to_next_snowman_melting_image()
        self.score = self.score + self.points_per_questions - self.opened_help_questions * 2
        self.health_points = 2
        self.opened_help_questions = 0

    def display_game_result(self):
        # Determine the result text
        result_text = "أحسنت! لقد فُزت!!" if self.isWin else "لقد خسرت!"
        text_surface = title_font.render(result_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Create a small window
        window_width, window_height = 400, 200
        window_surface = pygame.Surface((window_width, window_height))
        # Blit the background image onto the window surface
        window_surface.blit(SNOWMAN_GAME_RESULT, (0, 0))  # Draw the image at (0,0)

        # Optionally, draw a border around the window
        pygame.draw.rect(window_surface, (200, 200, 200), window_surface.get_rect(), 2)  # Gray border

        # Blit the result window onto the main screen
        window_rect = window_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(window_surface, window_rect)
        screen.blit(text_surface,
                    (window_rect.centerx - text_rect.width // 2, window_rect.centery - text_rect.height // 2))


# Main game loop
def validate_answer(snowman_current_game, answer_box):
    return snowman_current_game.get_current_correct_answer() == answer_box.text


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

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
