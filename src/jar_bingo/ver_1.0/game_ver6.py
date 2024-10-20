import random
from settings import *
from src.snowman.LLM import *
from data import *
from src.core.json_response_parser import *

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
    clicked_cells = [] #tracked clicked cells in the board to disable them after getting clicked.
    quiz_card_shown = False # track the state of the quiz card
    quiz_card_surface = pygame.Surface((QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT), pygame.SRCALPHA, 32)
    return (model, screen, font, board, clicked_cells, quiz_card_shown, quiz_card_surface)

# Function to create the game board
def create_board(board, font):
    board = [[(random.choice(prepositions_1), WHITE) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    return board

# Function to draw the game board
def draw_board(board, screen, font):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            cell_color = board[i][j][1]
            pygame.draw.rect(screen, cell_color, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # cell color fill
            pygame.draw.rect(screen, BLACK, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)  # Red border
            text = font.render(string_parser(board[i][j][0]), True, BLACK)
            text_rect = text.get_rect(center=(i * CELL_SIZE + CELL_SIZE // 2, j * CELL_SIZE + CELL_SIZE // 2))
            screen.blit(text, text_rect)

# Function to show the quiz card
def show_quiz_card(model, screen, font, preposition, choices, quiz_card_surface):
    quiz_card_shown = True
    #change to bring the qestions in bulk
    question_answer_pair =  get_questions(model, preposition, 1, preposition, "")
    print("question_answer_pair", question_answer_pair)
    quiz_question = question_answer_pair.get("sentence")
    correct_answer = question_answer_pair.get("correct_answer")
    quiz_choices = choices
    #Draw the quiz card
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - QUIZ_CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT))
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - QUIZ_CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT), 1)
    #pygame.draw.rect(quiz_card_surface, GREEN, (0, 0, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT))  # Green fill
    #pygame.draw.rect(quiz_card_surface, RED, (0, 0, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT), 2)  # Red border
    question_text = font.render(string_parser(quiz_question), True, BLACK)
    question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 50))
    screen.blit(question_text, question_rect)
    # blit card choices
    choice_rects = []
    for i, choice in enumerate(quiz_choices):
        choice_text = font.render(string_parser(choice), True, BLACK)
        choice_rect = choice_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 100 + i * 50))
        # pygame.draw.rect(screen, WHITE, (choice_rect.left - 10, choice_rect.top - 10, choice_rect.width + 100, choice_rect.height + 10))  # Green fill
        # pygame.draw.rect(screen, BLACK, (choice_rect.left - 10, choice_rect.top - 10, choice_rect.width + 100, choice_rect.height + 10), 2)  # Red border
        choices_size = pygame.Rect(10, 100 + i * (40 + 10), QUIZ_CARD_WIDTH - 20, 40)
        pygame.draw.rect(screen, WHITE, choices_size)  # Green fill
        pygame.draw.rect(screen, BLACK, choices_size, 2)  # Red border
        # pygame.draw.rect(screen, WHITE, (QUIZ_CARD_WIDTH // 2, QUIZ_CARD_HEIGHT // 2 , choice_rect.width + 100, choice_rect.height + 10))  # Green fill
        # pygame.draw.rect(screen, BLACK, (QUIZ_CARD_WIDTH // 2, QUIZ_CARD_HEIGHT // 2, choice_rect.width + 100, choice_rect.height + 10), 2)  # Red border
        screen.blit(choice_text, choice_rect)
        choice_rects.append(choice_rect)
    return quiz_card_shown, choice_rects
    # Draw the quiz card
    #pygame.draw.rect(quiz_card_surface, BLACK, (0, 0, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT))
    #question_text = font.render(string_parser(quiz_question), True, BLACK)
    #question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 50))
    #screen.blit(question_text, question_rect)
    #blit card choices
    #choice_rects = []
    #for i, choice in enumerate(quiz_choices):
        #choice_text = font.render(string_parser(choice), True, BLACK)
        #choice_rect = choice_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - QUIZ_CARD_HEIGHT // 2 + 100 + i * 50))
        #screen.blit(choice_text, choice_rect)
        #choice_rects.append(choice_rect)
    #return quiz_card_shown, choice_rects

# Function to check if a cell is clicked
def check_cell_click(pos):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i * CELL_SIZE < pos[0] < (i + 1) * CELL_SIZE and j * CELL_SIZE < pos[1] < (j + 1) * CELL_SIZE:
                return i, j
    return None

#pause the game
def pause(clock):
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: #enter key to resume
                    pause = False
            elif event.type == pygame.QUIT:
                pause = False
            else:
                clock.tick(0)

# Game loop
def main():
    #intialize game
    model, screen, font, board, clicked_cells, quiz_card_shown, quiz_card_surface = initialize_game()
    board = create_board(board, font)
    screen.fill(WHITE)
    draw_board(board, screen, font)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #pause game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #space key to pause
                    pause(clock)
            #user clicked on a cell in the board
            elif event.type == pygame.MOUSEBUTTONDOWN and not quiz_card_shown:
                clicked_cell = check_cell_click(event.pos) # check if the cell has been clicked before.
                if clicked_cell and all(i != clicked_cell for i in clicked_cells):
                    clicked_cells.append(clicked_cell)
                    preposition = board[clicked_cell[0]][clicked_cell[1]][0]
                    rest_of_prepositions = [element for element in prepositions_1 if element != preposition]
                    quiz_choices = [preposition] + random.sample(rest_of_prepositions, 2)
                    quiz_card_shown, choice_rects = show_quiz_card(model, screen, font, preposition, quiz_choices, quiz_card_surface)
            #user clicked a choice from the quiz card.
            elif event.type == pygame.MOUSEBUTTONDOWN and quiz_card_shown:
                #quiz_card_shown = False
                # Check if the clicked position is within any of the choice rectangles
                preposition = board[clicked_cell[0]][clicked_cell[1]][0]
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
                            correct_cell = clicked_cell
                        #color the cell of the correctly answered quiz.
                            board[correct_cell[0]][correct_cell[1]] = (board[correct_cell[0]][correct_cell[1]][0], GREEN)

                        else:
                            # Incorrect answer, do something
                            print("Incorrect!")
                            # Handle incorrect answer, e.g., show a message or deduct points
                            quiz_card_shown = False
                            incorrect_cell = clicked_cell
                            board[incorrect_cell[0]][incorrect_cell[1]] = (board[incorrect_cell[0]][incorrect_cell[1]][0], RED)

                if not quiz_card_shown:
                    screen.fill(WHITE)
                    draw_board(board, screen, font)

        pygame.display.flip()
    pygame.quit()
