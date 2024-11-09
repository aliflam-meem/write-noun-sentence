import os
import random

import mishkal.tashkeel
import pygame
from gtts import gTTS
from pygame import mixer

from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH, screen, body_font, SMALL_PADDING, LONG_PADDING, BUTTON_HEIGHT, \
    BUTTON_WIDTH, LOADING_IMAGE, BUTTON_FONT_COLOR, TITLE_HEIGHT, saddlebrown, thumbnail_width, IMAGE_WIDTH, \
    numbering_font, \
    YOU_WIN_AUDIO, YOU_LOST_AUDIO
from src.core.audio_player import play_sound, pause_background_sound
from src.core.utility import draw_score_and_health, draw_title, draw_button, load_image
from src.whack_a_mole.LLM import load_whack_a_mole_data
from src.whack_a_mole.constants import *


# from LLM import load_whack_a_mole_data

# ---------------------------------------
# Error Handling Functions
# ---------------------------------------
CWD = pathlib.Path(__file__).parent



def handle_font_load_error(font_name, size):
    print(f"Error loading font: {font_name} with size {size}")


def load_bomb_image():
    return load_image(CWD / 'assets/images/bomb.png', (100, 100))


def load_hole_image():
    return load_image(CWD / 'assets/images/hole.png', (120, 120))


def load_mole_image():
    return load_image(CWD / 'assets/images/mole2.png', (125, 125))


def load_background_image():
    return load_image(CWD / 'assets/images/background.png', (SCREEN_WIDTH, SCREEN_HEIGHT))


def load_mole_game_thumbnail():
    return load_image(CWD / 'assets/images/whack_a_mole_thumbnail.jpg', (thumbnail_width, thumbnail_width))


def load_background_tr_image():
    return load_image(CWD / 'assets/images/background_tr.png', (SCREEN_WIDTH, SCREEN_HEIGHT))


def check_if_sound_finished():
    if pygame.mixer.get_busy():
        return False
    else:
        return True

def play_audio(filename):
  """
  Plays an audio file using pygame.mixer.

  Args:
      filename (str): The path to the audio file (e.g., "audio_generated.mp3").
  """

  # Initialize the mixer if not already done
  if not mixer.get_init():
    mixer.init()

  # Load the song
  mixer.music.load(filename)

  # Set the volume (optional, adjust as needed)
  mixer.music.set_volume(0.7)

  # Start playing the song
  mixer.music.play()

def generate_gtts(text,number):
    try:
        pathlib.Path(CWD , 'assets/audio/gtts').mkdir(parents=True, exist_ok=True)
        pytts = gTTS(text, lang='ar')
        pytts.save( os.path.join(CWD , 'assets/audio/gtts/audio_generated_l'+ str(number) + '.mp3'))

    except Exception as e:
        print(f"Unexpected error saving gtts {text}: {e}")
        quit()

def whack_a_mole_play_audio(game):

            if  game.next_question_index == game.current_question_index and game.next_question_index<=len(game.questions):
                game.next_question_index+=1
                pause_background_sound(False)
                if  game.next_question_index > len(game.questions):
                    game.game_end = True
                    game.is_win = True

                else:
                    audio_1 = pygame.mixer.Sound(os.path.join(CWD , 'assets/audio/gtts/audio_generated_l1.mp3'))
                    audio_2 = pygame.mixer.Sound(os.path.join(CWD , 'assets/audio/gtts/audio_generated_l2.mp3'))
                    pause_background_sound(True)
                    audio_1.play()
                    while pygame.mixer.get_busy():
                        #pygame.time.delay(1)
                        pygame.event.poll()
                    audio_2.play()
                    while pygame.mixer.get_busy():
                        #pygame.time.delay(1)
                        pygame.event.poll()

# ---------------------------------------
# game components
# ---------------------------------------

class Hole:

    def __init__(self, num, col, row):
        self.num = num
        self.col = col
        self.row = row
        self.hole_image = load_hole_image()

    def draw(self):
        screen.blit(self.hole_image, (X_OFFSET + self.col * GRID_SIZE_X + 10,
                                      Y_OFFSET + self.row * GRID_SIZE_Y - 30))


class Mole:

    def __init__(self, mole_type):
        self.mole_type = mole_type
        self.mole_x = 0
        self.mole_y = 0
        self.word_x = 0
        self.word_y = 0
        self.speed = 1
        self.hole_num = 0
        self.hole_row = 0
        self.move = False
        self.counter = 0
        self.options = ['اسم', 'فعل', 'حرف']
        self.mole_image = load_mole_image()
        self.bomb_image = load_bomb_image()


    def select_hole(self, taken_holes):
        # Select a hole that is not taken
        self.hole_num = random.randint(0, 8)
        while self.hole_num in taken_holes:
            self.hole_num = random.randint(0, 8)

        col = self.hole_num % 3
        row = self.hole_num // 3
        self.word = self.options[col]
        self.hole_row = Y_OFFSET + row * GRID_SIZE_Y
        self.mole_x = X_OFFSET + GRID_SIZE_X * col - 40
        self.word_x = X_OFFSET + GRID_SIZE_X * col - 10
        self.mole_y = self.hole_row - 90
        self.word_y = self.hole_row - 80
        self.move = True
        self.counter = 0

    def draw(self):
        if self.move:
            if self.mole_type == 'mole':
                screen.blit(self.mole_image, (self.mole_x, self.mole_y))
                rendered_word = body_font.render(self.word, True, (0, 0, 0))
                screen.blit(rendered_word, (self.word_x, self.word_y))
            elif self.mole_type == 'bomb':
                screen.blit(self.bomb_image, (self.mole_x + 20, self.mole_y + 50))

    def show(self):
        if self.move:
            self.counter += 2

            # Mole is visible for 2 seconds
            if self.counter < 60:
                if self.mole_y > self.hole_row:
                    self.mole_y -= self.speed
                    self.word_y -= self.speed

            # Adjusted the y-coordinate
            elif self.mole_y < self.hole_row - 35:
                self.mole_y += self.speed * 2
                self.word_y += self.speed * 2

            else:
                self.move = False
                self.counter = 0

    def is_clicked(self, mouse_pos):
        # Check if the mole is clicked by the mouse
        if self.move:
            if self.mole_x - 75 < mouse_pos[
                0] < self.mole_x + 75 and self.mole_y < mouse_pos[
                1] < self.mole_y + 200:
                return True
        return False

    def clicked_answer(self):
        return self.word;


# ---------------------------------------
# Game class
# ---------------------------------------


class WhackaMoleGame:

    # def __init__(self,questions):
    def __init__(self):
        self.holes = []
        self.moles = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_over_counter = 0
        self.game_over_text = body_font
        self.game_end = False
        self.game_end_counter = 0
        self.score_text = body_font
        self.lives_text = body_font
        self.background = load_background_image()
        self.show_up_timer = 0
        self.show_up_end = 30
        self.is_data_loaded = False
        self.is_win = None
        self.max_score = 100
        self.game_stop = False
        #self.default_sound = True
        # self.question_item = {
        #    "sentence": "يجلسُ الطالبُ على المقعدِ",
        #    "word": "يجلس",
        #    "answer": "فعل"
        #  }
        self.questions = []
        '''
        self.questions = [
            {"sentence": "يجلسُ الطالبُ على المقعدِ", "word": "يجلس", "answer": "فعل"},
            {"sentence": "تقرأُ المعلمةُ الدرسَ", "word": "تقرأ", "answer": "فعل"},
            # ... add more question items here
        ]
        '''

        self.current_question_index = 0
        self.next_question_index  = 0
        self.generate_new_gtts = True

        for row in range(3):
            for col in range(3):
                self.holes.append(Hole(row * 3 + col, col, row))

        for mole in range(3):
            self.moles.append(Mole('mole'))

        self.bomb = Mole('bomb')

    def reset_game(self):
        self.holes = []
        self.moles = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_over_counter = 0
        self.game_end = False
        self.game_end_counter = 0
        self.show_up_timer = 0
        self.show_up_end = 100
        self.questions = []
        self.is_data_loaded = False
        self.is_win = None
        self.game_stop = False
        self.current_question_index = 0
        self.next_question_index  = 0
        self.generate_new_gtts = True

        for row in range(3):
            for col in range(3):
                self.holes.append(Hole(row * 3 + col, col, row))

        for mole in range(3):
            self.moles.append(Mole('mole'))

        self.bomb = Mole('bomb')


    def draw(self):

        for mole in self.moles:
            mole.draw()

        self.bomb.draw()

        for hole in self.holes:
            hole.draw()

        if self.current_question_index < len(self.questions):
            vocalizer = mishkal.tashkeel.TashkeelClass()
            question_item = self.questions[self.current_question_index]
            diacritic_sentense =  vocalizer.tashkeel(f"{question_item['sentence']}")
            question_text = [diacritic_sentense, "ما هو نوع قسم الكلام في كلمةِ "]

            question = []
            question_max_len = SMALL_PADDING + SCREEN_WIDTH / 3
            for line in question_text:
                question_dispaly = body_font.render(line, True, (0, 0, 0))
                question_max_len = max(SMALL_PADDING + SCREEN_WIDTH / 3, question_dispaly.get_width())
                question.append(question_dispaly)
            question_background_rect = pygame.Rect(SCREEN_WIDTH / 3 - SMALL_PADDING, WM_TITLE_HEIGHT + SMALL_PADDING / 4,
                                                   question_max_len, TITLE_HEIGHT - SMALL_PADDING)
            pygame.draw.rect(screen, (255, 255, 255), question_background_rect)
            for line in range(len(question)):
                screen.blit(question[line], (SCREEN_WIDTH / 2.5, WM_TITLE_HEIGHT + (LINES_SPACING * line)))

            diacritic_question_word = vocalizer.tashkeel(f"{question_item['word']}")
            question_word = f"({diacritic_question_word})"
            # print(rendered_question_word.get_width())
            rendered_question_word = body_font.render(question_word, True, (0, 0, 0))
            screen.blit(rendered_question_word, (SCREEN_WIDTH/2.5-rendered_question_word.get_width(), WM_TITLE_HEIGHT+LINES_SPACING))
            #screen.blit(rendered_question_word, (50, 50))
            question_text_l2 = [question_text[1], question_word]

            if self.generate_new_gtts:
                generate_gtts(question_text[0],1)
                generate_gtts(' '.join(question_text_l2),2)
                self.generate_new_gtts = False

        draw_score_and_health(10*self.score,x=900, y=10, health_points=self.lives, max_score=self.max_score , text_color=saddlebrown)


def display_game_result(self):

        background_tr = load_background_tr_image()
        screen.blit(background_tr, (0, 0))
        title = "لعبة أقسام الكلام"
        draw_title(title, title_color=BUTTON_FONT_COLOR, title_height=WM_TITLE_HEIGHT)

        back_button = draw_button("رجوع", 30, (WM_TITLE_HEIGHT - BUTTON_HEIGHT // 1.5) / 2,
                                  BUTTON_WIDTH - LONG_PADDING, BUTTON_HEIGHT // 1.5)

        message = "أحسنت!!" if self.is_win else "لقد خسرت!"
        message_color = GREEN if self.is_win else RED

        # Load the result image
        image_to_load = WIN_GAME_iMAGE if self.game_end else LOSE_GAME_IMAGE
        image = pygame.image.load(image_to_load)

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
        message_text = body_font.render(message, True,message_color)
        message_x = x + (IMAGE_WIDTH - message_text.get_width()) // 2
        message_y = y + (IMAGE_WIDTH - message_text.get_height()) // 2
        screen.blit(message_text, (message_x, message_y))

        # Display the score in the top-left corner within the image
        score_numbers_text = f"{self.max_score}/{10*self.score}"
        score_numbers_surface = numbering_font.render(score_numbers_text, True,message_color)
        score_numbers_rect = score_numbers_surface.get_rect(
            topleft=(message_x + message_text.get_width() / 3, message_y + SMALL_PADDING * 2)
        )
        screen.blit(score_numbers_surface, score_numbers_rect)
        audio = YOU_WIN_AUDIO if self.is_win else YOU_LOST_AUDIO
        if not self.game_stop:
            play_sound(audio)
            self.game_stop = True

# ---------------------------------------
# whack_a_mole_game_screen function
# ---------------------------------------

def whack_a_mole_game_screen(game):
    if not game.game_stop:
        pause_background_sound(False)
        screen.blit(game.background, (0, 0))
        title = "لعبة أقسام الكلام"
        draw_title(title, title_color=BUTTON_FONT_COLOR, title_height=WM_TITLE_HEIGHT)

        back_button = draw_button("رجوع", 30, (WM_TITLE_HEIGHT - BUTTON_HEIGHT // 1.5) / 2,
                                BUTTON_WIDTH - LONG_PADDING, BUTTON_HEIGHT // 1.5)

        #sound_button = screen.blit(SOUND_ON_IMAGE, (200, 10))
        if game.is_data_loaded == False:
            text = body_font.render('جار تحميل اللعبة', 1, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2 + SMALL_PADDING // 2,
                            SCREEN_HEIGHT // 2 - text.get_height() // 2 + LONG_PADDING))
            screen.blit(LOADING_IMAGE, (SCREEN_WIDTH * 0.5 - LONG_PADDING // 2, SCREEN_HEIGHT * 0.5 - LONG_PADDING))
            pygame.display.update()
            questions = load_whack_a_mole_data()
            game.questions = questions
            game.is_data_loaded = True

        screen.blit(game.background, (0, 0))
        draw_title(title, title_color=BUTTON_FONT_COLOR, title_height=WM_TITLE_HEIGHT)
        draw_button("رجوع", 30, (WM_TITLE_HEIGHT - BUTTON_HEIGHT // 1.5) / 2,
                                BUTTON_WIDTH - LONG_PADDING, BUTTON_HEIGHT // 1.5)
        game.draw()
        pygame.display.update()

        try:
            whack_a_mole_play_audio(game)
        except Exception as e:
            print(f"Error playing audio whack_a_mole_game: {e}")
            return

    return game
