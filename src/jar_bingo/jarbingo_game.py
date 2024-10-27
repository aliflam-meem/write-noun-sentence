import random
import pygame

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, screen
from src.core.json_response_parser import *
from src.core.audio_player import *
from src.jar_bingo.data import *
from src.jar_bingo.LLM import *
from src.jar_bingo.board import *
from src.jar_bingo.game_over import *

class JB_Game_Components:
    #class attributes: track game components changes.
    def __init__(self):
        # Game state variables
        self.model = set_model()
        self.board = []
        self.clicked_cells = []  # tracked clicked cells in the board to disable them after getting clicked.
        self.game_over = False
        self.quiz_card_shown = False  # track the state of the quiz card
        self.quiz_card_surface = pygame.Surface((QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT), pygame.SRCALPHA, 32)
        # sounds
        play_background_sound(BACKGROUND_SEA_SHP, volume=0.5)
        #img
        self.jellyfish_tiles = []  # board tiles
        self.background_image = initialize_imgs()
                # Draw on screen
        board = create_board(board, self.jellyfish_tiles)
        screen.fill(WHITE)
        draw_board(board, screen, self.background_image)

    def initialize_imgs(self):
        # Load images
        background_image = pygame.image.load(BACKGROUND_IMG)  # Replace with the actual path to your image
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        blue_jellyfish_img = pygame.image.load(BLUE_JELLYFISH_TILE)
        blue_jellyfish_img = pygame.transform.scale(blue_jellyfish_img, (CELL_SIZE, CELL_SIZE))  # Resize
        green_jellyfish_img = pygame.image.load(GREEN_JELLYFISH_TILE)
        green_jellyfish_img = pygame.transform.scale(green_jellyfish_img, (CELL_SIZE, CELL_SIZE))  # Resize
        red_jellyfish_img = pygame.image.load(RED_JELLYFISH_TILE)
        red_jellyfish_img = pygame.transform.scale(red_jellyfish_img, (CELL_SIZE, CELL_SIZE))  # Resize
        self.jellyfish_tiles.append(blue_jellyfish_img)
        self.jellyfish_tiles.append(green_jellyfish_img)
        self.jellyfish_tiles.append(red_jellyfish_img)
        return background_image
    