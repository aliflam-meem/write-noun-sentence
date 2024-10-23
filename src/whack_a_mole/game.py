import os
import sys
from gtts import gTTS
import time
import pathlib
import pygame
from pygame import mixer
import random
# from LLM import load_data
from src.constants import *
from src.whack_a_mole.constants import *
from src.core.utility import draw_score_and_health, draw_title, draw_button

# from LLM import load_whack_a_mole_data

# ---------------------------------------
# Error Handling Functions
# ---------------------------------------
CWD = pathlib.Path(__file__).parent



def handle_image_load_error(file_name):
    print(f"Error loading image: {file_name}")


def handle_font_load_error(font_name, size):
    print(f"Error loading font: {font_name} with size {size}")


def load_image(filename, size):
    """Loads and scales an image.

    Args:
        filename (str): The name of the image file.
        size (tuple): The desired width and height of the scaled image.

    Returns:
        pygame.Surface: The loaded and scaled image surface.
    """

    try:
        image_file_name = pygame.image.load(filename)
        image = pygame.transform.scale(image_file_name, size)
        return image
    except FileNotFoundError:
        handle_image_load_error(filename)
        quit()
    except Exception as e:
        print(f"Unexpected error loading image {filename}: {e}")
        quit()


def load_bomb_image():
    return load_image(CWD / 'assets/images/bomb.png', (100, 100))


def load_hole_image():
    return load_image(CWD / 'assets/images/hole.png', (120, 120))


def load_mole_image():
    return load_image(CWD / 'assets/images/mole2.png', (125, 125))


def load_background_image():
    return load_image(CWD / 'assets/images/background.png', (SCREEN_WIDTH, SCREEN_HEIGHT - 50))

#def load_win_image():
#    return load_image(CWD / 'assets/Win.png',(400,400))

def check_if_sound_finished():
    if  pygame.mixer.get_busy():
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
        pytts = gTTS(text, lang='ar')
        pytts.save( os.path.join(CWD , 'assets/audio/gtts/audio_generated_l'+ str(number) + '.mp3'))

    except Exception as e:
        print(f"Unexpected error saving gtts {text}: {e}")
        quit()

def whack_a_mole_play_audio(game):
            audio_1 = pygame.mixer.Sound(os.path.join(CWD , 'assets/audio/gtts/audio_generated_l1.mp3'))  
            audio_2 = pygame.mixer.Sound(os.path.join(CWD , 'assets/audio/gtts/audio_generated_l2.mp3'))  
            if  game.next_question_index == game.current_question_index and game.next_question_index<=len(game.questions):
                game.next_question_index+=1
                if  game.next_question_index > len(game.questions):
                    game.game_end = True

                else:
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
        self.speed = 3
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
            self.counter += 1

            # Mole is visible for 2 seconds
            if self.counter < 120:
                if self.mole_y > self.hole_row:
                    self.mole_y -= self.speed
                    self.word_y -= self.speed

            # Adjusted the y-coordinate
            elif self.mole_y < self.hole_row:
                self.mole_y += self.speed * 3
                self.word_y += self.speed * 3

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
        self.show_up_end = 100

        # self.question_item = {
        #    "sentence": "يجلسُ الطالبُ على المقعدِ",
        #    "word": "يجلس",
        #    "answer": "فعل"
        #  }
        # """
        self.questions = [
            {"sentence": "يجلسُ الطالبُ على المقعدِ", "word": "يجلس", "answer": "فعل"},
            {"sentence": "تقرأُ المعلمةُ الدرسَ", "word": "تقرأ", "answer": "فعل"},
            # ... add more question items here
        ]
        # """
        # self.questions = questions

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

            question_item = self.questions[self.current_question_index]
            question_text = [f"{question_item['sentence']}", "ما هو نوع قسم الكلام في كلمة "]

            question = []
            question_max_len = SMALL_PADDING + SCREEN_WIDTH / 3
            for line in question_text:
                question_dispaly = body_font.render(line, True, (0, 0, 0))
                question_max_len = max(SMALL_PADDING + SCREEN_WIDTH / 3, question_dispaly.get_width())
                question.append(question_dispaly)
            question_background_rect = pygame.Rect(SCREEN_WIDTH / 3 - SMALL_PADDING, TITLE_HEIGHT + SMALL_PADDING / 4,
                                                   question_max_len, TITLE_HEIGHT - SMALL_PADDING)
            pygame.draw.rect(screen, (255, 255, 255), question_background_rect)
            for line in range(len(question)):
                screen.blit(question[line], (SCREEN_WIDTH / 2.5, TITLE_HEIGHT + (LINES_SPACING * line)))

            question_word = f"( {question_item['word']} )"
            # print(rendered_question_word.get_width())
            rendered_question_word = body_font_bold.render(question_word, True, (0, 0, 0))
            screen.blit(rendered_question_word, (SCREEN_WIDTH/2.5-rendered_question_word.get_width(), TITLE_HEIGHT+LINES_SPACING))
            #screen.blit(rendered_question_word, (50, 50))
            question_text_l2 = [question_text[1], question_word] 

            if self.generate_new_gtts:
                generate_gtts(question_text[0],1)
                generate_gtts(' '.join(question_text_l2),2)
                self.generate_new_gtts = False
            

        draw_score_and_health(10*self.score,x=900, y=10, health_points=self.lives, max_score=100 , text_color=saddlebrown)

        if self.game_over:
            text = self.game_over_text.render('حظ أوفر في المرة القادمة', 1, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                               SCREEN_HEIGHT //  2 - text.get_height() // 2))
            
        if self.game_end:
            text = self.game_over_text.render('انتهت اللعبة', 1, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                               SCREEN_HEIGHT //  2 - text.get_height() // 2))
            


# ---------------------------------------
# whack_a_mole_game_screen function
# ---------------------------------------

def whack_a_mole_game_screen(game):
    try:
        title = "لعبة أقسام الكلام"
        draw_title(title, color=BUTTON_FONT_COLOR, title_height=TITLE_HEIGHT)

        back_button = draw_button("رجوع", 30, (TITLE_HEIGHT - BUTTON_HEIGHT // 1.5 ) / 2,
                                                BUTTON_WIDTH - LONG_PADDING, BUTTON_HEIGHT // 1.5 )
        
        # questions = load_whack_a_mole_data()
        # game = Game(questions)

        screen.blit(game.background, (0, 60))
        game.draw()
        pygame.display.update()
        whack_a_mole_play_audio(game) 

        return game


    except Exception as e:
        print(f"Error initializing whack_a_mole_game: {e}")
        return
