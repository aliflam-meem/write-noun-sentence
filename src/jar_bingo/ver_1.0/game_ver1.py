import random

import pygame
from settings import *


# Pygame initialization
def inititalize_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)  # Fill the screen with white background
    pygame.display.set_caption("Preposition Quiz Game")
    # Font and colors
    font = pygame.font.Font(None, 36)
    # Game state variables
    board = []
    clicked_cells = []
    quiz_card_shown = False
    correct_answer = None
    board = create_board(board)
    return (screen, font, board, clicked_cells, quiz_card_shown, correct_answer)


# Function to create the game board
def create_board(board):
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            board[i][j] = random.choice(prepositions)
    return board


# Function to draw the game board
def draw_board(board, screen, font):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            pygame.draw.rect(screen, WHITE, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            text = font.render(board[i][j], True, BLACK)
            text_rect = text.get_rect(center=(i * CELL_SIZE + CELL_SIZE // 2, j * CELL_SIZE + CELL_SIZE // 2))
            screen.blit(text, text_rect)


# Function to show the quiz card
def show_quiz_card(screen, font, question, choices):
    quiz_card_shown = True
    quiz_question = question
    quiz_choices = choices
    correct_answer = choices[0]  # Assuming the first choice is correct
    # Draw the quiz card
    pygame.draw.rect(screen, GRAY, (
        SCREEN_WIDTH // 2 - QUIZ_CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2, QUIZ_CARD_WIDTH,
        QUIZ_CARD_HEIGHT))
    question_text = font.render(quiz_question, True, BLACK)
    question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 50))
    screen.blit(question_text, question_rect)
    print("just blit")
    for i, choice in enumerate(quiz_choices):
        choice_text = font.render(choice, True, BLACK)
        choice_rect = choice_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 100 + i * 50))
        screen.blit(choice_text, choice_rect)
    return quiz_card_shown


# Function to check if a cell is clicked
def check_cell_click(pos):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i * CELL_SIZE < pos[0] < (i + 1) * CELL_SIZE and j * CELL_SIZE < pos[1] < (j + 1) * CELL_SIZE:
                return i, j
    return None


def jumpscare(screen):
    font = pygame.font.Font(None, 50)
    text = font.render("Message Displayed", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)


# Game loop
def main():
    # intialize game
    screen, font, board, clicked_cells, quiz_card_shown, correct_answer = inititalize_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not quiz_card_shown:
                clicked_cell = check_cell_click(event.pos)
                if clicked_cell and not any(i == clicked_cell for i in clicked_cells):
                    clicked_cells.append(clicked_cell)
                    preposition = board[clicked_cell[0]][clicked_cell[1]]
                    print("if clicked_cell and all(i != clicked_cell for i in clicked_cells)", preposition)
                    prep_index = prepositions.index(preposition)
                    quiz_choices = [preposition] + random.sample(prepositions, 2)
                    print("if clicked_cell and all(i != clicked_cell for i in clicked_cells)", quiz_choices)
                    quiz_card_shown = show_quiz_card(screen, font, quiz_questions[prep_index], quiz_choices)
                # Update the display
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN and quiz_card_shown:
                quiz_card_shown = False
                # Check if the clicked choice is correct
                clicked_choice = event.pos[1] - (SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 100)
                clicked_choice_index = clicked_choice // 50
                print("clicked_choice = event.pos[1] - (SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 100)",
                      clicked_choice_index)
                if clicked_choice_index == 0:  # First choice is correct
                    board[clicked_cell[0]][clicked_cell[1]] = 'O'  # Clear the cell
                    pygame.draw.rect(screen, GREEN,
                                     (clicked_cell[0] * CELL_SIZE, clicked_cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:  # Wrong choice
                    pygame.draw.rect(screen, RED,
                                     (clicked_cell[0] * CELL_SIZE, clicked_cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                # Update the display
                pygame.display.flip()

        # Redraw the board after closing the quiz card
        screen.fill(WHITE)
        draw_board(board, screen, font)
        pygame.display.flip()

    pygame.quit()


# Run the game
if __name__ == "__main__":
    main()
