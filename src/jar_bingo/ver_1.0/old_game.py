import pygame
import random
import time

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 100
BOARD_SIZE = 3  # Initial board size
QUIZ_CARD_WIDTH = 400
QUIZ_CARD_HEIGHT = 300

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Preposition Quiz Game")

# Font and colors
font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Game state variables
board = []
clicked_cells = []
quiz_card_shown = False
quiz_question = None
quiz_choices = []
correct_answer = None

# Function to create the game board
def create_board(size):
    global board
    board = [[None for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            board[i][j] = random.choice(prepositions)

# Function to draw the game board
def draw_board():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            pygame.draw.rect(screen, WHITE, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            text = font.render(board[i][j], True, BLACK)
            text_rect = text.get_rect(center=(i * CELL_SIZE + CELL_SIZE // 2, j * CELL_SIZE + CELL_SIZE // 2))
            screen.blit(text, text_rect)

# Function to show the quiz card
def show_quiz_card(question, choices):
    global quiz_card_shown, quiz_question, quiz_choices, correct_answer
    quiz_card_shown = True
    quiz_question = question
    quiz_choices = choices
    correct_answer = choices[0]  # Assuming the first choice is correct

    # Draw the quiz card
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - QUIZ_CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT))
    question_text = font.render(quiz_question, True, BLACK)
    question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 50))
    screen.blit(question_text, question_rect)

    for i, choice in enumerate(quiz_choices):
        choice_text = font.render(choice, True, BLACK)
        choice_rect = choice_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 100 + i * 50))
        screen.blit(choice_text, choice_rect)

# Function to check if a cell is clicked
def check_cell_click(pos):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i * CELL_SIZE < pos[0] < (i + 1) * CELL_SIZE and j * CELL_SIZE < pos[1] < (j + 1) * CELL_SIZE:
                return i, j
    return None

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not quiz_card_shown:
            clicked_cell = check_cell_click(event.pos)
            if clicked_cell and clicked_cell not in clicked_cells:
                clicked_cells.append(clicked_cell)
                preposition = board[clicked_cell[0]][clicked_cell[1]]
                show_quiz_card(quiz_questions[preposition], [preposition] + random.sample(prepositions, 2))
        elif event.type == pygame.MOUSEBUTTONDOWN and quiz_card_shown:
            quiz_card_shown = False
            # Check if the clicked choice is correct
            # ... (Implement your logic to check the answer)

    screen.fill(WHITE)
    draw_board()

    if quiz_card_shown:
        show_quiz_card(quiz_question, quiz_choices)

    pygame.display.flip()

pygame.quit()