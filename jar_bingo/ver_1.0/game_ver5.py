import pygame
import random
import time
from settings import *
from LLM import *
from data import *
from jar_bingo.jar_bingo_response_parser import *

# Pygame initialization
def initialize_game():
    model = set_model()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Preposition Quiz Game")
    # Font and colors
    font = pygame.font.Font('Arial.ttf', 32)
    # Game state variables
    board = []
    clicked_cells = []  # tracked clicked cells in the board to disable them after getting clicked.
    quiz_card_shown = False  # track the state of the quiz card
    quiz_card_surface = pygame.Surface((QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT))
    #correct_audio = pygame.mixer.Sound("")
    correct_audio = ""
    return (model, screen, font, board, clicked_cells, quiz_card_shown, quiz_card_surface, correct_audio)

# Function to create the game board
def create_board(board, font):
    board = [[(random.choice(prepositions_1), WHITE) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    return board

# Function to draw the game board
def draw_board(board, screen, font):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j][1] != None:
                cell_color = board[i][j][1]
            else:
                cell_color = BLACK
            pygame.draw.rect(screen, cell_color, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), width=3)
            text = font.render(string_parser(board[i][j][0]), True, BLACK)
            text_rect = text.get_rect(center=(i * CELL_SIZE + CELL_SIZE // 2, j * CELL_SIZE + CELL_SIZE // 2))
            screen.blit(text, text_rect)

# Function to show the quiz card
def show_quiz_card(model, font, preposition, choices, screen, quiz_card_surface):
    quiz_card_shown = True
    #change to bring the qestions in bulk
    question_answer_pair = get_questions(model, preposition, 1, preposition, "")
    quiz_question = question_answer_pair.get("sentence")
    correct_answer = question_answer_pair.get("correct_answer")
    quiz_choices = choices
    # Draw the quiz card
    card = pygame.Rect(0, 0, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT)
    pygame.draw.rect(quiz_card_surface, WHITE, card)  # Draw a black border
    question_text = font.render(string_parser(quiz_question), True, BLACK)
    question_rect = question_text.get_rect(center=(QUIZ_CARD_WIDTH // 2, 50))
    quiz_card_surface.blit(question_text, question_rect)

   # Create choice rectangles with a wider width and a black border
    choice_rect_width = QUIZ_CARD_WIDTH - 20  # Adjust the width as needed
    choice_rect_height = 40
    choice_rects = []
    #screen.blit(quiz_card_surface, (SCREEN_WIDTH // 2 - QUIZ_CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2))
    for i, choice in enumerate(quiz_choices):
        choice_text = font.render(string_parser(choice), True, BLACK)
        choice_rect = pygame.Rect(10, 100 + i * (choice_rect_height + 10), choice_rect_width, choice_rect_height)
        #pygame.draw.rect(quiz_card_surface, WHITE, choice_rect)  # Draw a white background for the choice rectangle
        pygame.draw.rect(quiz_card_surface, RED, choice_rect)  # Draw a black border
        choice_text_rect = choice_text.get_rect(center=choice_rect.center) #Adjust the choice text position to center within the choice rectangle
        # Draw the choice rectangle and text after the quiz card
        quiz_card_surface.blit(quiz_card_surface, (0, 0))  # Blit the quiz card first
        quiz_card_surface.blit(choice_text, choice_text_rect)
        choice_rects.append(choice_rect)
    screen.blit(quiz_card_surface, (SCREEN_WIDTH // 2 - QUIZ_CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2))
    return quiz_card_shown, choice_rects

# Function to check if a cell is clicked
def check_cell_click(pos):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i * CELL_SIZE < pos[0] < (i + 1) * CELL_SIZE and j * CELL_SIZE < pos[1] < (j + 1) * CELL_SIZE:
                return i, j
    return None

# Pause the game
def pause(clock):
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key to resume
                    pause = False
            elif event.type == pygame.QUIT:
                pause = False
            else:
                clock.tick(0)

# Game loop
def main():
    # Initialize game
    model, screen, font, board, clicked_cells, quiz_card_shown, quiz_card_surface, correct_audio = initialize_game()
    board = create_board(board, font)
    screen.fill(WHITE)
    draw_board(board, screen, font)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space key to pause
                    pause(clock)
            #user clicked on a cell in the board
            elif event.type == pygame.MOUSEBUTTONDOWN and not quiz_card_shown:
                clicked_cell = check_cell_click(event.pos)
                if clicked_cell and clicked_cell not in clicked_cells:
                    clicked_cells.append(clicked_cell)
                    preposition = board[clicked_cell[0]][clicked_cell[1]][0]
                    rest_of_prepositions = [element for element in prepositions_1 if element != preposition]
                    quiz_choices = [preposition] + random.sample(rest_of_prepositions, 2)
                    random.shuffle(quiz_choices)
                    quiz_card_shown, choice_rects = show_quiz_card(model, font, preposition, quiz_choices, screen, quiz_card_surface)
            elif event.type == pygame.MOUSEBUTTONDOWN and quiz_card_shown:
                quiz_card_shown = False
                 # Check if the clicked position is within any of the choice rectangles
                preposition = board[clicked_cell[0]][clicked_cell[1]][0]
                # Check if the clicked position is within the quiz card's bounding rectangle
                quiz_card_rect = pygame.Rect(SCREEN_WIDTH // 2 - QUIZ_CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT)
                #if quiz_card_rect.collidepoint(event.pos):
                     # Check if the clicked position is within any of the choice rectangles (before iterating)
                click_on_choice = False
                for i, choice_rect in enumerate(choice_rects):
                    print("for i, choice_rect in enumerate(choice_rects)", i)
                    if choice_rect.collidepoint(event.pos):
                        click_on_choice = True
                        # User selected a choice
                        selected_choice = quiz_choices[i]
                        print("selected choice: ",selected_choice)
                        # Check if the selected choice is correct
                        if selected_choice == preposition:
                            print("Correct!")
                            # Hide the quiz card and update the game state accordingly
                            quiz_card_shown = False
                            correct_cell = clicked_cell
                            #color the cell of the correctly answered quiz.
                            board[correct_cell[0]][correct_cell[1]] = (board[correct_cell[0]][correct_cell[1]][0], GREEN)
                            break  # Exit the loop after a successful click
                        else:
                            print("Incorrect!")
                            # Handle incorrect answer, e.g., show a message or deduct points
                            quiz_card_shown = False
                            incorrect_cell = clicked_cell
                            #color the cell of the incorrectly answered quiz.
                            board[incorrect_cell[0]][incorrect_cell[1]] = (board[incorrect_cell[0]][incorrect_cell[1]][0], RED)
                            break  # Exit the loop after a successful click

                if not click_on_choice: #user clicked outside the card but the card is still open.
                    # User clicked outside any choice rectangle but within the card (handle this case)
                    print("User clicked outside any choice")
                    quiz_card_shown = True  # Keep the card open
            #else:
                #user clicked outside the card but the card is still open.
                #quiz_card_shown = True

            if not quiz_card_shown:
                screen.fill(WHITE)
                draw_board(board, screen, font)
            #else:
                #screen.blit(quiz_card_surface, (SCREEN_WIDTH // 2 - QUIZ_CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2))


        pygame.display.flip()
    pygame.quit()