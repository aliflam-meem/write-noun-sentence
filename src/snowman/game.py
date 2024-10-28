import re

import pygame
from thefuzz import fuzz

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, screen, IMAGE_WIDTH, YOU_WIN_AUDIO, YOU_LOST_AUDIO, \
    body_font, RED, GREEN, numbering_font, SMALL_PADDING
from src.core.audio_player import play_sound
from src.core.utility import format_questions_count_string
from src.snowman.LLM import load_game_data
from src.snowman.constants import snowman_levels, snowman_levels_keys, snowman_working_directory, SNOWMAN_GAME_RESULT


class SnowmanGame:

    def __init__(self, level=snowman_levels_keys[2], questions_count=1):
        self.max_score = 100
        self.help_question_index = 0
        self.is_win = None
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
        self.max_questions_count_per_type = 4
        self.information = ""
        self.is_correct_answer_displayed = False
        self.is_result_sound_played = False
        self.load_melting_snowman_images()

    def reset_game(self):
        self.is_win = None
        self.question_index = 0
        self.score = 0
        self.health_points = 2
        self.opened_help_questions = 0
        self.num_of_wrong_answers = 0
        self.reset_melting_image_index()
        self.questions = []
        self.reset_information()
        self.reset_is_answer_displayed()
        self.reset_help_question_index()
        self.reset_is_result_sound_played()

    def reset_is_result_sound_played(self):
        self.is_result_sound_played = False

    def reset_is_answer_displayed(self):
        self.is_correct_answer_displayed = False

    def reset_information(self):
        self.information = ""

    def reset_melting_image_index(self):
        self.melting_image_index = 0

    def reset_help_question_index(self):
        self.help_question_index = 0

    def get_current_information(self):
        return self.information

    def increase_wrong_answers(self):
        self.num_of_wrong_answers += 1

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
            questions_count_as_string = format_questions_count_string(questions_to_generate)

            # Load the question data for the current batch
            questions_data = load_game_data(noun_type, questions_count_as_string)

            # Retry if questions_data is not valid (loop until a valid dictionary or list is returned)
            while type(questions_data) is bool:
                questions_data = load_game_data(noun_type, questions_count_as_string)

            # Process the questions depending on their type (list or dictionary)
            if isinstance(questions_data, dict):
                # Format and update the dictionary directly
                self.format_questions_data(questions_data)
                questions.append(questions_data)  # Store the formatted question
            elif isinstance(questions_data, list):
                # Process each question in the list
                for question_dict in questions_data:
                    self.format_questions_data(question_dict)  # Format each question
                questions.extend(questions_data)  # Add all formatted questions to the list

        return questions

    def format_questions_data(self, question_dict):
        # Strip the correct answer and clean up
        question_dict["correct_answer"] = question_dict["correct_answer"].strip()

        # Format the question text (replace series of periods with underscores)
        question = question_dict["question"]
        question = re.sub(r'(\.\.\.)+', "_______ ", question)

        # Determine the number of words in the correct answer
        num_of_answer_words = len(question_dict["correct_answer"].split())

        # Choose the appropriate Arabic word count description
        if num_of_answer_words == 1:
            num_words = "كلمة واحدة"
        elif num_of_answer_words == 2:
            num_words = "كلمتين"
        else:
            num_words = "أكثر من كلمتين"

        # Format the question text with the word count description
        question = f"املأ الفراغ التالي ب{num_words} بالمبتدأ المناسب.\n{question}"

        # Update the formatted question back into the dictionary
        question_dict["question"] = question

    def initialize_game_with_questions(self):
        for n_type in snowman_levels[self.level]["noun_types"]:
            self.questions.extend(self.generate_questions_data(n_type))

    def load_melting_snowman_images(self):
        img = pygame.image.load(snowman_working_directory / 'assets/images/complete.png')
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load(snowman_working_directory / 'assets/images/melting_1.png')
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load(snowman_working_directory / 'assets/images/melting_2.png')
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load(snowman_working_directory / 'assets/images/melting_3.png')
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load(snowman_working_directory / 'assets/images/melting_4.png')
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load(snowman_working_directory / 'assets/images/melted.png')
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)


    def get_current_question(self):
        return f"السؤال ({self.question_index + 1}) \n{self.questions[self.question_index]['question']}"

    def get_current_correct_answer(self):
        return self.questions[self.question_index]["correct_answer"]

    def get_current_help_questions(self):
        return self.questions[self.question_index]["help_questions"]

    def get_all_open_help_questions(self):
        open_questions = ""
        for i in range(self.help_question_index + 1):
            open_questions += f"{i + 1}- {self.get_current_help_questions()[i]} \n"
        return open_questions

    def get_current_grammar(self):
        return self.questions[self.question_index]["grammar"]

    def get_current_melting_snowman_image(self):
        return self.melting_snowman_images[self.melting_image_index]

    def are_all_answers_wrong(self):
        return self.num_of_wrong_answers == len(self.melting_snowman_images) - 1

    def is_game_over(self):
        return self.are_all_answers_wrong() or self.reached_last_question()

    def reached_last_question(self):
        return self.question_index == len(self.questions) - 1

    def move_to_next_snowman_melting_image(self):
        self.melting_image_index = self.melting_image_index if self.melting_image_index == len(
            self.melting_snowman_images) - 1 else self.melting_image_index + 1

    def move_to_next_help_question(self):
        self.opened_help_questions += 1
        self.help_question_index = self.help_question_index if self.help_question_index == 2 else self.help_question_index + 1

    def move_to_next_question(self):
        self.question_index += 1
        if not self.is_correct_answer_displayed:
            self.score += self.points_per_questions - self.opened_help_questions * 2
        self.health_points = 2
        self.opened_help_questions = 0
        self.help_question_index = 0
        self.reset_information()
        self.reset_is_answer_displayed()
        self.reset_help_question_index()

    def display_game_result(self):
        message = "أحسنت!!" if self.is_win else "لقد خسرت!"
        message_color = GREEN if self.is_win else RED

        # Load the result image
        image = pygame.image.load(SNOWMAN_GAME_RESULT)

        # Scale the image to half the screen size
        image = pygame.transform.scale(image, (IMAGE_WIDTH, IMAGE_WIDTH))

        # Calculate the image position to center it
        x = (SCREEN_WIDTH - IMAGE_WIDTH) // 2
        y = (SCREEN_HEIGHT - IMAGE_WIDTH) // 1.5 - SMALL_PADDING

        # Define the border size and color
        BORDER_SIZE = 10
        BORDER_COLOR = (100, 100, 100)  # Adjust to your preferred border color
        BORDER_RADIUS = 20  # Adjust the corner roundness here

        # Create a rounded rectangle for the border
        border_rect = pygame.Rect(x - BORDER_SIZE, y - BORDER_SIZE,
                                  IMAGE_WIDTH + 2 * BORDER_SIZE, IMAGE_WIDTH + 2 * BORDER_SIZE)
        pygame.draw.rect(screen, BORDER_COLOR, border_rect, border_radius=BORDER_RADIUS)

        # Blit the main image onto the screen, centered within the border
        screen.blit(image, (x, y))

        # Render the result message and center it within the image
        message_text = body_font.render(message, True, message_color)
        message_x = x + (IMAGE_WIDTH - message_text.get_width()) // 2
        message_y = y + (IMAGE_WIDTH - message_text.get_height()) // 2
        screen.blit(message_text, (message_x, message_y))

        # Display the score in the top-left corner within the image
        score_numbers_text = f"{self.max_score}/{self.score}"
        score_numbers_surface = numbering_font.render(score_numbers_text, True, message_color)
        score_numbers_rect = score_numbers_surface.get_rect(
            topleft=(message_x + message_text.get_width() / 3, message_y + SMALL_PADDING * 2)
        )
        screen.blit(score_numbers_surface, score_numbers_rect)

    def melt_the_snowman(self):
        self.melting_image_index = len(self.melting_snowman_images) - 1

    def set_correct_answer_as_information(self):
        self.information = "إليك الإجابة الصحيحة: " + self.get_current_correct_answer()
        self.is_correct_answer_displayed = True


    def set_help_questions_as_information(self):
        self.information = "إليك بعض الأسئلة المساعدة على تخمين الإجابة الصحيحة:" + "\n" + self.get_all_open_help_questions()
        self.move_to_next_help_question()

    def set_grammar_as_information(self):
        self.information = f"القاعدة \n {self.get_current_grammar()}"

    def can_submit_answer(self):
        return not (self.is_correct_answer_displayed and self.are_all_answers_wrong())

    def can_proceed_to_next_question(self):
        return not self.is_game_over()

    def finalize_game(self):
        if self.are_all_answers_wrong():
            self.score -= self.opened_help_questions * 2
        elif not self.are_all_answers_wrong() and not self.is_correct_answer_displayed:
            self.score += self.points_per_questions - self.opened_help_questions * 2
        if self.score < 0:
            self.score = 0
        self.is_win = self.num_of_wrong_answers < len(self.melting_snowman_images) - 1

    def play_result_sound(self):
        audio = YOU_WIN_AUDIO if self.is_win else YOU_LOST_AUDIO
        play_sound(audio)

    def display_result_and_play_sound(self):
        self.display_game_result()
        if not self.is_result_sound_played:
            self.is_result_sound_played = True
            self.play_result_sound()

    def is_answer_valid(self, answer_box):
        print("get_current_correct_answer ", self.get_current_correct_answer())
        return fuzz.ratio(self.get_current_correct_answer(), answer_box.text.strip()) == 100
