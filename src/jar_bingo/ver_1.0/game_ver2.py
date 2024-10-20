import random

import pygame
from settings import *


# Pygame initialization

def inititalize_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Preposition Quiz Game")

    # Font and colors
    font = pygame.font.Font(None, 32)

    # Game state variables
    board = []
    clicked_cells = []
    quiz_card_shown = False
    correct_answer = None
    return (screen, font, board, clicked_cells, quiz_card_shown, correct_answer)


# Function to create the game board

def create_board(board):
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            board[i][j] = random.choice(prepositions)

    return board


# Function to draw the game board

def draw_board(board, screen, font, correct_cell=None, incorrect_cell=None):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            cell_color = WHITE
            if correct_cell and (i, j) == correct_cell:
                cell_color = GREEN  # Replace GREEN with your desired green color
            elif incorrect_cell and (i, j) == incorrect_cell:
                cell_color = RED  # Replace RED with your desired red color
            pygame.draw.rect(screen, cell_color, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
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
    pygame.draw.rect(screen, WHITE, (
        SCREEN_WIDTH // 2 - QUIZ_CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2, QUIZ_CARD_WIDTH,
        QUIZ_CARD_HEIGHT))
    question_text = font.render(quiz_question, True, BLACK)
    question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 50))
    screen.blit(question_text, question_rect)

    choice_rects = []
    for i, choice in enumerate(quiz_choices):
        choice_text = font.render(choice, True, BLACK)
        choice_rect = choice_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 100 + i * 50))
        screen.blit(choice_text, choice_rect)
        choice_rects.append(choice_rect)

    return quiz_card_shown, choice_rects


# Function to check if a cell is clicked

def check_cell_click(pos):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i * CELL_SIZE < pos[0] < (i + 1) * CELL_SIZE and j * CELL_SIZE < pos[1] < (j + 1) * CELL_SIZE:
                return i, j
    return None


# Game loop

def main():
    # intialize game
    screen, font, board, clicked_cells, quiz_card_shown, correct_answer = inititalize_game()
    board = create_board(board)
    screen.fill(WHITE)
    draw_board(board, screen, font)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not quiz_card_shown:
                clicked_cell = check_cell_click(event.pos)
                if clicked_cell and all(i != clicked_cell for i in clicked_cells):
                    clicked_cells.append(clicked_cell)
                    preposition = board[clicked_cell[0]][clicked_cell[1]]
                    prep_index = prepositions.index(preposition)
                    quiz_choices = [preposition] + random.sample(prepositions, 2)
                    quiz_card_shown, choice_rects = show_quiz_card(screen, font, quiz_questions[prep_index],
                                                                   quiz_choices)
            elif event.type == pygame.MOUSEBUTTONDOWN and quiz_card_shown:
                quiz_card_shown = False
                # Check if the clicked position is within any of the choice rectangles
                preposition = board[clicked_cell[0]][clicked_cell[1]]
                for i, choice_rect in enumerate(choice_rects):
                    if choice_rect.collidepoint(event.pos):
                        # User selected a choice
                        selected_choice = quiz_choices[i]

                        # Check if the selected choice is correct
                        if selected_choice == preposition:
                            # Correct answer, do something
                            print("Correct!")
                            # Hide the quiz card and update the game state accordingly
                            quiz_card_shown = False
                            screen.fill(WHITE)
                            draw_board(board, screen, font, correct_cell=clicked_cell)
                        else:
                            # Incorrect answer, do something
                            print("Incorrect!")
                            # Handle incorrect answer, e.g., show a message or deduct points
                            quiz_card_shown = False
                            screen.fill(WHITE)
                            draw_board(board, screen, font, incorrect_cell=clicked_cell)

            # screen.fill(WHITE)
            # draw_board(board, screen, font)
            # if quiz_card_shown:
            #    quiz_card_shown = show_quiz_card(screen, font, quiz_questions[prep_index], quiz_choices)

        pygame.display.flip()
    pygame.quit()


# Run the game

if __name__ == "__main__":
    main()
