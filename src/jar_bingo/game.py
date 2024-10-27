import pygame
from src.jar_bingo.settings import JR_TITLE_HEIGHT
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_FONT_COLOR, screen, RED, GAMES_BOARD_SCREEN, JAR_BINGO_GAME
from src.core.utility import draw_title, draw_back_button
from src.core.json_response_parser import *
from src.core.audio_player import *
from src.jar_bingo.data import *
from src.jar_bingo.LLM import *
from src.jar_bingo.board import *
from src.jar_bingo.game_over import *
from src.jar_bingo.game_utils import *



class JBGameComponents:
    #class attributes: track game components changes.
    def __init__(self):
        #initialize Game state variables
        self.game_state = "initialized"
        self.model = set_model()
        self.board = []
        self.clicked_cells = []  # tracked clicked cells in the board to disable them after getting clicked.
        self.game_over = False
        self.quiz_card_shown = False  # track the state of the quiz card
        self.quiz_choices = []
        #self.quiz_card_surface = pygame.Surface((QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT), pygame.SRCALPHA, 32)
        #initialize imgs
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

    def reset_game(self):
        #initialize Game state variables
        self.game_state = "initialized"
        self.board = []
        self.clicked_cells = []  # tracked clicked cells in the board to disable them after getting clicked.
        self.game_over = False
        self.quiz_card_shown = False  # track the state of the quiz card
        self.quiz_choices = []
        #self.quiz_card_surface = pygame.Surface((QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT), pygame.SRCALPHA, 32)
        #initialize imgs
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
        draw_title(title, title_color=WHITE, title_height=JR_TITLE_HEIGHT)
        back_button = draw_back_button()
    #Main
    def play_jarbingo_game(self, running, back_button, main_game_state):
    # start game
        if self.game_state == "initialized":
            #redraw game screen
            self.draw_bingo_screen()
        clock = pygame.time.Clock()
        #pause_background_sound(False)
        #initialize sounds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return running, main_game_state
            # pause game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # space key to pause
                    self.game_state = "paused"
                    pause(clock)
            elif event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
                    main_game_state = GAMES_BOARD_SCREEN
                    return running, main_game_state
            # user clicked on a cell in the board
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.quiz_card_shown:
                clicked_cell = check_cell_click(event.pos)  # check if the cell has been clicked before.
                if clicked_cell and all(i != clicked_cell for i in self.clicked_cells):
                    self.clicked_cells.append(clicked_cell)
                    print("clicked_cell: ", clicked_cell)
                    preposition = self.board[clicked_cell[0]][clicked_cell[1]][0]
                    self.quiz_card_shown, self.choice_rects, self.quiz_choices, correct_answer = show_quiz_card(self.model,self.quiz_card_shown, preposition)
                    #compare requested preposition and correct answer
                    print(preposition, correct_answer)
            # user clicked a choice from the quiz card.
            elif event.type == pygame.MOUSEBUTTONDOWN and self.quiz_card_shown:
                # Check if the clicked position is within any of the choice rectangles
                clicked_cell = check_cell_click(event.pos)
                preposition = self.board[clicked_cell[0]][clicked_cell[1]][0]
                for i, choice_rect in enumerate(self.choice_rects):
                    if choice_rect.collidepoint(event.pos):
                        # User selected a choice
                        selected_choice = self.quiz_choices[i]
                        # Check if the selected choice is correct
                        if selected_choice == self.board[clicked_cell[0]][clicked_cell[1]][0]:
                            # Correct answer, do something
                            print("Correct!")
                            # Hide the quiz card and update the game state accordingly
                            self.quiz_card_shown = False
                            correct_cell = clicked_cell
                            # Color the cell of the correctly answered quiz
                            self.board[correct_cell[0]][correct_cell[1]] = (
                                self.board[correct_cell[0]][correct_cell[1]][0], self.jellyfish_tiles[1],
                                GREEN)  # board[correct_cell[0]][correct_cell[1]][2])
                            if (check_win(self.board)):
                                print("You won")
                                self.game_over = True
                                self.game_state = "win"
                        else:
                            # Incorrect answer, do something
                            print("Incorrect!")
                            # Handle incorrect answer, e.g., show a message or deduct points
                            self.quiz_card_shown = False
                            incorrect_cell = clicked_cell
                            # Color the cell of the incorrectly answered quiz
                            self.board[incorrect_cell[0]][incorrect_cell[1]] = (
                                self.board[incorrect_cell[0]][incorrect_cell[1]][0], self.jellyfish_tiles[2], RED)
                            if (check_lose(self.board)):
                                print("You lose!")
                                self.game_over = True
                                self.game_state = "lose"

                if not self.quiz_card_shown:
                    self.draw_bingo_screen()
                if self.game_over:
                    if self.game_state == "win":
                        game_over_card(WIN_MENU_IMG, GREEN, True, score = 10, max_score=10)
                    elif self.game_state == "lose":
                        game_over_card(LOSE_MENU_IMG, RED, False, score = 0, max_score=10)
            pygame.display.flip()
        return running, main_game_state
        