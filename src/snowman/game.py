import re

import pygame

from src.constants import title_font, SCREEN_WIDTH, SCREEN_HEIGHT, screen, IMAGE_WIDTH
from src.core.utility import format_questions_count_string
from src.snowman.LLM import load_game_data
from src.snowman.constants import snowman_levels, snowman_levels_keys, snowman_working_directory


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
        img = pygame.image.load(snowman_working_directory / "assets/images/complete.png")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load(snowman_working_directory / "assets/images/melting_1.png")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load(snowman_working_directory / "assets/images/melting_2.png")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load(snowman_working_directory / "assets/images/melting_3.png")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load(snowman_working_directory / "assets/images/melting_4.png")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        img = pygame.image.load(snowman_working_directory / "assets/images/melted.jpg")
        img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_WIDTH))
        self.melting_snowman_images.append(img)
        print(snowman_working_directory)


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

    def display_game_result(self, SNOWMAN_GAME_RESULT=None):
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
