import queue
import re
import time
from concurrent.futures import ThreadPoolExecutor

import pygame
from thefuzz import fuzz

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, screen, IMAGE_WIDTH, YOU_WIN_AUDIO, YOU_LOST_AUDIO, \
    body_font, RED, GREEN, numbering_font, SMALL_PADDING
from src.core.audio_player import play_sound
from src.core.output import append_string_to_file
from src.core.utility import format_questions_count_string
from src.snowman.LLM import load_game_data, set_model
from src.snowman.constants import snowman_levels, snowman_levels_keys, snowman_working_directory, SNOWMAN_GAME_RESULT, \
    snow_melting_sound


class SnowmanGame:

    def __init__(self, level=snowman_levels_keys[2], questions_count=1):
        # Flag to track if the user clicked "Next" but no new question is ready
        self.elapsed_time_model = 0
        self.is_sound_on = False
        self.executor = ThreadPoolExecutor(max_workers=2)  # Create a thread pool with 2 workers
        self.llm_thread = None  # Future to hold the result of the LLM thread
        self.output_queue = queue.Queue()
        self.LLM_model = None
        self.levels_keys = snowman_levels_keys
        self.waiting_for_next_question = False
        self.max_score = 100
        self.help_question_index = 0
        self.is_win = None
        self.points_per_questions = 10
        self.total_questions_count = 10
        self.melting_snowman_images = []
        self.melting_image_index = 0
        self.questions = []
        self.question_index = 0
        self.score = 0
        self.health_points = 2
        self.opened_help_questions = 0
        self.num_of_wrong_answers = 0
        self.is_user_answer_correct = False
        self.level = level
        self.questions_count_per_type = questions_count
        self.max_questions_count_per_type = 4
        self.information = ""
        self.is_correct_answer_displayed = False
        self.is_result_sound_played = False
        # Start the question generation in a separate thread
        self.start_setting_llm_model_thread()
        self.load_melting_snowman_images()

    def reset_game(self):
        self.is_win = None
        self.question_index = 0
        self.score = 0
        self.health_points = 2
        self.opened_help_questions = 0
        self.num_of_wrong_answers = 0
        self.reset_melting_image_index()
        self.reset_questions_list()
        self.reset_information()
        self.reset_is_answer_displayed()
        self.reset_is_user_answer_correct()
        self.reset_help_question_index()
        self.reset_is_result_sound_played()
        self.start_question_generation_thread()

    def reset_questions_list(self):
        self.questions = []

    def reset_is_result_sound_played(self):
        self.is_result_sound_played = False

    def reset_is_answer_displayed(self):
        self.is_correct_answer_displayed = False

    def reset_is_user_answer_correct(self):
        self.is_user_answer_correct = False


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

    def start_question_generation_thread(self):
        print("start_question_generation_thread")

        # Check if LLM model is being set
        if self.llm_thread and not self.llm_thread.done():
            print("Waiting for LLM model to be set...")
            self.llm_thread.result()  # This will block until the LLM model setup is complete
            elapsed_time_model = time.time() - self.start
            string_to_append = f'********* \nThe time elapsed for setting up the snowman model is {elapsed_time_model}'
            append_string_to_file(string_to_append, snowman_working_directory / 'assets/files/latency.txt')

        # Now check if the model is set
        if not self.LLM_model:
            self.LLM_model = self.output_queue.get()
            print(" done setting llm ", self.LLM_model)

        # Start question generation using the executor
        self.start = time.time()
        self.executor.submit(self.initialize_game_with_questions)


    def start_setting_llm_model_thread(self):
        print("start_setting_llm_model_thread")
        # Submit the LLM model setup to the executor
        self.start = time.time()
        self.llm_thread = self.executor.submit(set_model, self.output_queue)

    def generate_questions_data(self, noun_type, total_questions_count=None):
        print("generate_questions_data")
        # Initialize the list to store all questions
        questions = []

        # Process the questions in chunks of x number
        total_questions_count = self.questions_count_per_type if total_questions_count is None else total_questions_count

        # Generate questions in batches of 5 until we run out of questions
        print("range(0, total_questions_count, self.max_questions_count_per_type) ",
              range(0, total_questions_count, self.max_questions_count_per_type))
        for i in range(0, total_questions_count, self.max_questions_count_per_type):
            # Determine how many questions to generate in the current batch
            questions_to_generate = min(self.max_questions_count_per_type, total_questions_count - i)
            print("questions_to_generate ", questions_to_generate)
            # Format the questions count string (assuming it's for UI or logging)
            questions_count_as_string = format_questions_count_string(questions_to_generate)

            # Load the question data for the current batch
            questions_data = load_game_data(self.LLM_model, noun_type, questions_count_as_string)

            # Retry if questions_data is not valid (loop until a valid dictionary or list is returned)
            while type(questions_data) is bool:
                questions_data = load_game_data(self.LLM_model, noun_type, questions_count_as_string)

            # Process the questions depending on their type (list or dictionary)
            if isinstance(questions_data, dict):
                print(isinstance(questions_data, dict))
                # Format and update the dictionary directly
                self.format_questions_data(questions_data)
                questions.append(questions_data)  # Store the formatted question
            elif isinstance(questions_data, list):
                print(isinstance(questions_data, list))
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
            print(n_type)
            self.questions.extend(self.generate_questions_data(n_type))

        # Get the first noun type from the current level
        first_noun_type = snowman_levels[self.level]["noun_types"][0]
        # If more questions are needed, genrate more questions so the list reaches the desired count
        if len(self.questions) < self.total_questions_count:
            needed_count = self.total_questions_count - len(self.questions)
            print("needed_count", needed_count)
            self.questions.extend(self.generate_questions_data(first_noun_type, needed_count))
        elapsed_time_generation = time.time() - self.start
        string_to_append = f'The time elapsed for generating {self.total_questions_count} question is {elapsed_time_generation}'
        append_string_to_file(string_to_append, snowman_working_directory / 'assets/files/latency.txt')

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
        if len(self.questions) == 0:
            return ""
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
        print("self.question_index ", self.question_index)
        return self.question_index == self.total_questions_count - 1

    def move_to_next_snowman_melting_image(self):
        self.melting_image_index = self.melting_image_index if self.melting_image_index == len(
            self.melting_snowman_images) - 1 else self.melting_image_index + 1
        if self.melting_image_index < len(self.melting_snowman_images) - 1:
            play_sound(snow_melting_sound, fade_ms=50)

    def move_to_next_help_question(self):
        self.opened_help_questions += 1
        self.help_question_index = self.help_question_index if self.help_question_index == 2 else self.help_question_index + 1

    def move_to_next_question(self):
        if self.question_index < len(self.questions) - 1:
            self.question_index += 1
            if not self.is_correct_answer_displayed:
                if self.is_user_answer_correct:
                    self.score += self.points_per_questions - self.opened_help_questions * 2
                else:
                    self.score -= self.opened_help_questions * 2
            self.health_points = 2
            self.opened_help_questions = 0
            self.help_question_index = 0
            self.reset_information()
            self.reset_is_answer_displayed()
            self.reset_is_user_answer_correct()
            self.reset_help_question_index()
            self.waiting_for_next_question = False

            # Set flag to wait for the next question if there isn't one yet and we haven't reached max questions
        elif len(self.questions) < self.total_questions_count:
            self.waiting_for_next_question = True

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
            topleft=(message_x + message_text.get_width() / 4, message_y + SMALL_PADDING * 2)
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

    # def generate_initial_questions(self):
    #     for level in self.levels_keys:
    #         # Format the questions count string (assuming it's for UI or logging)
    #         questions_count_as_string = format_questions_count_string(2)
    #
    #         noun_type = snowman_levels[level]["noun_types"][0]
    #         # Load the question data for the current batch
    #         questions_data = load_game_data(self.LLM_model, noun_type, questions_count_as_string)
    #
    #         # Retry if questions_data is not valid (loop until a valid dictionary or list is returned)
    #         while type(questions_data) is bool:
    #             questions_data = load_game_data(self.LLM_model, noun_type, questions_count_as_string)
    #
    #         # Process the questions depending on their type (list or dictionary)
    #         with self.lock_questions_list:
    #             if isinstance(questions_data, dict):
    #                 # Format and update the dictionary directly
    #                 self.format_questions_data(questions_data)
    #                 self.initial_questions[level].append(questions_data)  # Store the formatted question
    #                 self.new_question_added_event.set()  # Signal that a new question is ready
    #                 self.new_question_added_event.clear()
    #             elif isinstance(questions_data, list):
    #                 # Process each question in the list
    #                 for question_dict in questions_data:
    #                     self.format_questions_data(question_dict)  # Format each question
    #                     self.initial_questions[level].extend(questions_data)  # Add all formatted questions to the list
    #                     self.new_question_added_event.set()  # Signal that a new question is ready
    #                     self.new_question_added_event.clear()
    #
    #     self.start_question_generation_thread()
