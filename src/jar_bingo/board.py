import random

import pygame

from src.constants import SCREEN_WIDTH, GREEN, screen
from src.jar_bingo.data import *
from src.jar_bingo.settings import *


# Function to create the game board
def create_board(board, jellyfish_tiles):
    # board = [[(random.choice(prepositions_1), LIGHT_BLUE3) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board = [[(random.choice(prepositions_1), jellyfish_tiles[0], LIGHT_BLUE3) for _ in range(BOARD_SIZE)] for _ in
             range(BOARD_SIZE)]
    return board

# Function to draw the game board
def draw_board(board, background_image):
    screen.blit(background_image,
                (SCREEN_WIDTH - background_image.get_width(), 0))  # (0, 0))  # Blit the background image
    pygame.draw.rect(screen, WHITE, (BOARD_PADDING - 4, BOARD_PADDING + 2, BOARD_WIDTH + 6, BOARD_HEIGHT + 4), 5)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # print(board[i][j][1])
            fill_cell = board[i][j][1]
            color_cell = board[i][j][2]
            # No need to draw text as prepositions are replaced with images
            pygame.draw.rect(screen, color_cell, (
            BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING + j * CELL_SIZE, CELL_SIZE,
            CELL_SIZE))  # (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # cell color fill
            pygame.draw.rect(screen, DARK_BLUE1,
                             (BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING + j * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                             2)  # (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)  # border
            # Blit the jellyfish image on each cell
            screen.blit(fill_cell, (BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING + j * CELL_SIZE))


# Checks for a win condition based on diagonal, vertical, and horizontal matches
def check_win(board):
    """
    of green jellyfish tiles.
    Args:
        board: A 2D list representing the game board, where each element is a tuple
               containing the preposition, jellyfish image, and color.
    Returns:
        True if a win is detected, False otherwise.
      Logic:
          The function iterates through the entire board to check for consecutive green jellyfish matches in three directions:
          Horizontal: Scans each row from left to right.
          Vertical: Scans each column from top to bottom.
          Diagonal: Scans both upward-left and downward-right diagonals.
      Diagonal Checks:
          The function iterates through the board starting from the top-left corner, ensuring that there are enough cells to form a diagonal line of WIN_LENGTH.
          For each starting position, it checks both upward-left and downward-right diagonals.
          The inner loop iterates through the diagonal cells, incrementing consecutive_green if the current cell contains a green jellyfish.
          If consecutive_green reaches WIN_LENGTH, a win is detected.
          This modified function effectively checks for wins in all directions without relying on the last clicked cell, making it more robust and adaptable for different game scenarios.
    """
    # Check horizontal matches
    for row in range(BOARD_SIZE):
        consecutive_green = 0
        for col in range(BOARD_SIZE):
            if board[row][col][2] == GREEN:
                consecutive_green += 1
                if consecutive_green == WIN_LENGTH:
                    return True
            else:
                consecutive_green = 0

    # Check vertical matches
    for col in range(BOARD_SIZE):
        consecutive_green = 0
        for row in range(BOARD_SIZE):
            if board[row][col][2] == GREEN:
                consecutive_green += 1
                if consecutive_green == WIN_LENGTH:
                    return True
            else:
                consecutive_green = 0

    # Check diagonal matches (both directions)
    for i in range(BOARD_SIZE - WIN_LENGTH + 1):
        for j in range(BOARD_SIZE - WIN_LENGTH + 1):
            # Check upward-left diagonal
            consecutive_green = 0
            for k in range(WIN_LENGTH):
                if board[i + k][j + k][2] == GREEN:
                    consecutive_green += 1
                else:
                    break
            if consecutive_green == WIN_LENGTH:
                return True

            # Check downward-right diagonal
            consecutive_green = 0
            for k in range(WIN_LENGTH):
                if board[i + k][j + WIN_LENGTH - 1 - k][2] == GREEN:
                    consecutive_green += 1
                else:
                    break
            if consecutive_green == WIN_LENGTH:
                return True
    print("consecutive_green", consecutive_green)
    return False


def check_lose(board):
    """
    This function checks if all cells in the board have been clicked.

    Args:
        board: A 2D list representing the game board. Each cell contains a tuple of (preposition, jellyfish_image, color).

    Returns:
        True if all cells have been clicked, False otherwise.
    """
    for row in board:
        for cell in row:
            # Check if the cell color is not the default light blue (unclicked) and the second element (jellyfish image) is not the default one (blue jellyfish)
            if cell[2] == LIGHT_BLUE3:
                return False
    return True
