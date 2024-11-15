from src.constants import RED, GAMES_BOARD_SCREEN, ORANGE
from src.core.utility import draw_title, draw_back_button, draw_score_and_health, \
    draw_sound_button
import pygame
from src.jar_bingo.constants import JR_TITLE_HEIGHT
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, screen, RED, GAMES_BOARD_SCREEN, ORANGE, maroon
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, screen, RED, GAMES_BOARD_SCREEN, ORANGE, maroon
from src.core.utility import draw_title, draw_back_button, draw_button, load_loading_image, draw_score_and_health
from src.core.json_response_parser import *
from src.core.audio_player import *
from src.jar_bingo.data import *
from src.jar_bingo.LLM import *
from src.jar_bingo.board import *
from src.jar_bingo.game_over import *
from src.jar_bingo.game_utils import *


class JBGameComponents:

    # class attributes: track game components changes.
    def __init__(self):
        # initialize Game state variables
        self.game_state = "initialized"
        self.loading = False
        self.board = []
        self.clicked_cells = []  # tracked clicked cells in the board to disable them after getting clicked.
        self.clicked_cell = None
        self.game_over = False
        self.quiz_card_shown = False  # track the state of the quiz card
        self.quiz_choices = []
        self.correct_answer = ""
        self.model = None
        self.sexual_beh_and_racism_detection_model = None
        self.score = 0
        # bg sound button
        self.music_button = None
        # self.music_button = pygame.image.load(BG_MUSIC_BUTTON)
        # self.music_button = pygame.transform.scale(self.music_button, (80, 80))
        self.bg_sound = True
        # initialize imgs
        self.jellyfish_tiles = []  # board tiles
        self.background_image = None
        self.initialize_imgs()
        # Draw on screen
        self.board = create_board(self.board, self.jellyfish_tiles)
        self.choice_rects = None

    def initialize_imgs(self):
        # Load images
        self.background_image = pygame.image.load(BACKGROUND_IMG)  # Replace with the actual path to your image
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        blue_jellyfish_img = pygame.image.load(BLUE_JELLYFISH_TILE)
        blue_jellyfish_img = pygame.transform.scale(blue_jellyfish_img, (CELL_SIZE, CELL_SIZE))  # Resize
        green_jellyfish_img = pygame.image.load(GREEN_JELLYFISH_TILE)
        green_jellyfish_img = pygame.transform.scale(green_jellyfish_img, (CELL_SIZE, CELL_SIZE))  # Resize
        red_jellyfish_img = pygame.image.load(RED_JELLYFISH_TILE)
        red_jellyfish_img = pygame.transform.scale(red_jellyfish_img, (CELL_SIZE, CELL_SIZE))  # Resize
        self.jellyfish_tiles.append(blue_jellyfish_img)
        self.jellyfish_tiles.append(green_jellyfish_img)
        self.jellyfish_tiles.append(red_jellyfish_img)

    def restart_game(self, jar_bingo_initial):
        if jar_bingo_initial:
            # redraw game screen
            self.draw_bingo_screen()
            load_loading_image(text_message='جار تحميل اللعبة', text_color=WHITE, scale_x=200, scale_y=200)
            self.model = set_model()
            #self.sexual_beh_and_racism_detection_model = set_sexual_beh_and_racism_detection_model()
        # initialize Game state variables
        self.game_state = "restart"
        self.loading = False
        self.board = []
        self.clicked_cells = []  # tracked clicked cells in the board to disable them after getting clicked.
        self.clicked_cell = None
        self.game_over = False
        self.quiz_card_shown = False  # track the state of the quiz card
        self.quiz_choices = []
        self.correct_answer = ""
        self.score = 0
        # bg sound button
        # self.music_button = pygame.image.load(BG_MUSIC_BUTTON)
        # self.music_button = pygame.transform.scale(self.music_button, (80, 80))
        self.bg_sound = True
        # initialize imgs
        self.jellyfish_tiles = []  # board tiles
        self.background_image = None
        self.initialize_imgs()
        # Draw on screen
        self.board = create_board(self.board, self.jellyfish_tiles)
        self.choice_rects = None

    def draw_bingo_screen(self):
        screen.fill(WHITE)
        draw_board(self.board, self.background_image)
        self.game_state = "running"
        title = "لعبة بنغو أحرف الجر في المحيط"
        draw_title(title, title_height=JR_TITLE_HEIGHT, title_color=WHITE, padding=200, border_radius=25,
                   background_color=DARK_TEAL)
        draw_back_button(button_height=30)
        # score and health
        draw_score_and_health(self.score, x=900, y=70, health_points=3, max_score=100, text_color=TURQUOISE_BLUE)
        # draw music button
        self.music_button = draw_sound_button(SCREEN_WIDTH - 100, 10, 60, 50, border_color=DARK_TEAL,
                                              text_color=TURQUOISE_BLUE, button_color=DARK_TEAL, highlight_color=BLACK,
                                              radius=5)

    # Main
    def play_jar_bingo_game(self, running, back_button, main_game_state):
        # start game
        self.game_state = "running"
        clock = pygame.time.Clock()
        # initialize sounds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return running, main_game_state, self.bg_sound
            # bg sound on/off
            elif event.type == pygame.MOUSEBUTTONDOWN and self.music_button.collidepoint(event.pos):
                if self.bg_sound:
                    print("pausing the bg sound.")
                    pause_background_sound(True)
                    self.bg_sound = False
                else:
                    print("resuming the bg sound.")
                    pause_background_sound(False)
                    self.bg_sound = True
            # Back to games menu
            elif event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
                main_game_state = GAMES_BOARD_SCREEN
                return running, main_game_state, self.bg_sound
            # game in progress
            elif not self.game_over:
                # user clicked on a cell in the board
                # pause game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # space key to pause
                        self.game_state = "paused"
                        pause(clock)
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.quiz_card_shown:
                    self.clicked_cell = check_cell_click(event.pos)  # check if the cell has been clicked before.
                    if self.clicked_cell and all(i != self.clicked_cell for i in self.clicked_cells):
                        self.clicked_cells.append(self.clicked_cell)
                        print("clicked_cell: ", self.clicked_cell)
                        preposition = self.board[self.clicked_cell[0]][self.clicked_cell[1]][0]
                        self.quiz_card_shown, self.choice_rects, self.quiz_choices, self.correct_answer = show_quiz_card(
                            self.model, self.sexual_beh_and_racism_detection_model, self.quiz_card_shown, preposition)
                        # compare requested preposition and correct answer
                        print("preposition & correct answer: ",preposition, self.correct_answer)
                # user clicked a choice from the quiz card.
                elif event.type == pygame.MOUSEBUTTONDOWN and self.quiz_card_shown:
                    # Check if the clicked position is within any of the choice rectangles
                    preposition = self.board[self.clicked_cell[0]][self.clicked_cell[1]][0]
                    for i, choice_rect in enumerate(self.choice_rects):
                        if choice_rect.collidepoint(event.pos):
                            # User selected a choice
                            selected_choice = self.quiz_choices[i]
                            # Check if the selected choice is correct
                            if selected_choice == self.correct_answer: #self.board[self.clicked_cell[0]][self.clicked_cell[1]][0]:
                                # Correct answer, do something
                                print("Correct!")
                                # Hide the quiz card and update the game state accordingly
                                self.quiz_card_shown = False
                                correct_cell = self.clicked_cell
                                # Color the cell of the correctly answered quiz
                                self.board[correct_cell[0]][correct_cell[1]] = (
                                    self.board[correct_cell[0]][correct_cell[1]][0], self.jellyfish_tiles[1], GREEN)
                                self.score = self.score + 5
                                # reset the value
                                self.clicked_cell = None
                                if (check_win(self.board)):
                                    print("You won")
                                    self.game_over = True
                                    self.game_state = "win"
                                if (check_lose(self.board)):
                                    print("You lose!")
                                    self.game_over = True
                                    self.game_state = "lose"
                                if (check_lose(self.board)):
                                    print("You lose!")
                                    self.game_over = True
                                    self.game_state = "lose"
                            else:
                                # Incorrect answer, do something
                                print("Incorrect!")
                                # Handle incorrect answer, e.g., show a message or deduct points
                                self.quiz_card_shown = False
                                incorrect_cell = self.clicked_cell
                                # Color the cell of the incorrectly answered quiz
                                self.board[incorrect_cell[0]][incorrect_cell[1]] = (
                                    self.board[incorrect_cell[0]][incorrect_cell[1]][0], self.jellyfish_tiles[2], RED)
                                # reset the value
                                self.clicked_cell = None
                                if (check_lose(self.board)):
                                    print("You lose!")
                                    self.game_over = True
                                    self.game_state = "lose"
                                if (check_win(self.board)):
                                    print("You won")
                                    self.game_over = True
                                    self.game_state = "win"
                                if (check_win(self.board)):
                                    print("You won")
                                    self.game_over = True
                                    self.game_state = "win"

                if not self.quiz_card_shown and not self.game_over:
                    self.draw_bingo_screen()
                if self.game_over:
                    if self.game_state == "win":
                        self.draw_bingo_screen()
                        game_over_card(WIN_MENU_IMG, LIGHT_GREEN, True, score=self.score, max_score=100)
                        self.game_state = "game_over"

                    elif self.game_state == "lose":
                        self.draw_bingo_screen()
                        game_over_card(LOSE_MENU_IMG, ORANGE, False, score = self.score, max_score=100)
                        self.game_state = "game_over"
                        game_over_card(LOSE_MENU_IMG, ORANGE, False, score = self.score, max_score=100)
                        self.game_state = "game_over"
                    else:
                        print("waiting for the player")

            pygame.display.flip()
        return running, main_game_state, self.bg_sound
