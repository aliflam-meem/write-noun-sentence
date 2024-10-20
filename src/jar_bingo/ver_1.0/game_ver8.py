import random

from LLM import *
from board import *
from data import *
from game_over import *
from settings import *

from src.core.json_response_parser import *


# Pygame initialization
def initialize_game():
    model = set_model()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Preposition Quiz Game")
    # Font and colors
    font = pygame.font.Font('fonts/Arial.ttf', 32)
    # Game state variables
    board = []
    clicked_cells = []  # tracked clicked cells in the board to disable them after getting clicked.
    quiz_card_shown = False  # track the state of the quiz card
    game_over = False
    jellyfish_tiles = []  # board tiles
    quiz_card_surface = pygame.Surface((QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT), pygame.SRCALPHA, 32)
    # Load images
    background_image = pygame.image.load(
        "images/Gemini_Generated_Image_5ivjha5ivjha5ivj.jfif")  # Replace with the actual path to your image
    background_image = pygame.transform.scale(background_image, (
        SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to half the screen width for demonstration
    # Load the images
    blue_jellyfish_img = pygame.image.load("images/Gemini_Generated_Image_b7o9wwb7o9wwb7o9 (1).jfif", )
    blue_jellyfish_img = pygame.transform.scale(blue_jellyfish_img, (CELL_SIZE, CELL_SIZE))  # Resize
    green_jellyfish_img = pygame.image.load("images/Gemini_Generated_Image_3n68uq3n68uq3n68.jfif", )
    green_jellyfish_img = pygame.transform.scale(green_jellyfish_img, (CELL_SIZE, CELL_SIZE))  # Resize
    red_jellyfish_img = pygame.image.load("images/Gemini_Generated_Image_501zw2501zw2501z.jfif", )
    red_jellyfish_img = pygame.transform.scale(red_jellyfish_img, (CELL_SIZE, CELL_SIZE))  # Resize
    jellyfish_tiles.append(blue_jellyfish_img)
    jellyfish_tiles.append(green_jellyfish_img)
    jellyfish_tiles.append(red_jellyfish_img)

    return (
        model, screen, font, board, clicked_cells, quiz_card_shown, quiz_card_surface, background_image,
        jellyfish_tiles,
        game_over)


# Function to draw the game board
def draw_board(board, screen, background_image):
    screen.blit(background_image,
                (SCREEN_WIDTH - background_image.get_width(), 0))  # (0, 0))  # Blit the background image
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


# Function to show the quiz card
def show_quiz_card(model, screen, font, preposition, choices, quiz_card_surface):
    quiz_card_shown = True
    # change to bring the qestions in bulk
    question_answer_pair = get_questions(model, preposition, 1, preposition, "")
    print("question_answer_pair", question_answer_pair)
    quiz_question = question_answer_pair.get("sentence")
    correct_answer = question_answer_pair.get("correct_answer")
    quiz_choices = choices
    # Draw the quiz card
    pygame.draw.rect(screen, WHITE, (QUIZ_CARD_PADDING, QUIZ_CARD_PADDING + 20, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT))
    pygame.draw.rect(screen, DARK_BLUE1, (QUIZ_CARD_PADDING, QUIZ_CARD_PADDING + 20, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT),
                     3)
    # question and choices
    question_text = font.render(string_parser(quiz_question), True, BLACK)
    question_rect = question_text.get_rect(
        center=(QUIZ_CARD_WIDTH // 2 + 100, 120 + (CHOICE_RECT_HEIGHT + CHOICE_RECT_PADDING)))
    screen.blit(question_text, question_rect)
    # blit card choices
    choice_rects = []
    for i, choice in enumerate(quiz_choices):
        choice_text = font.render(string_parser(choice), True, BLACK)
        choices_size = pygame.Rect(QUIZ_CARD_PADDING + 100, QUIZ_CARD_HEIGHT + (40 * i),
                                   QUIZ_CARD_WIDTH - 2 * QUIZ_CARD_PADDING, CHOICE_RECT_HEIGHT)
        choice_rect = choice_text.get_rect(
            center=(choices_size.left + choices_size.width // 2, choices_size.top + choices_size.height // 2))
        pygame.draw.rect(screen, LIGHT_BLUE3, choices_size)  # choice fill
        pygame.draw.rect(screen, DARK_BLUE1, choices_size, 3)  # choice border
        screen.blit(choice_text, choice_rect)
        choice_rects.append(choice_rect)
    return quiz_card_shown, choice_rects, correct_answer


# Function to check if a cell is clicked
def check_cell_click(pos):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i * CELL_SIZE < pos[0] < (i + 1) * CELL_SIZE and j * CELL_SIZE < pos[1] < (j + 1) * CELL_SIZE:
                return i, j
    return None


# pause the game
def pause(clock):
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # enter key to resume
                    pause = False
            elif event.type == pygame.QUIT:
                pause = False
            else:
                clock.tick(0)


# Game loop
def main():
    # intialize game
    model, screen, font, board, clicked_cells, quiz_card_shown, quiz_card_surface, background_image, jellyfish_tiles, game_over = initialize_game()
    board = create_board(board, jellyfish_tiles)
    screen.fill(WHITE)
    draw_board(board, screen, background_image)
    clock = pygame.time.Clock()
    game_state = "running"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # pause game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # space key to pause
                    game_state = "paused"
                    pause(clock)
            # user clicked on a cell in the board
            elif event.type == pygame.MOUSEBUTTONDOWN and not quiz_card_shown:
                clicked_cell = check_cell_click(event.pos)  # check if the cell has been clicked before.
                if clicked_cell and all(i != clicked_cell for i in clicked_cells):
                    clicked_cells.append(clicked_cell)
                    preposition = board[clicked_cell[0]][clicked_cell[1]][0]
                    rest_of_prepositions = [element for element in prepositions_1 if element != preposition]
                    quiz_choices = [preposition] + random.sample(rest_of_prepositions, 2)
                    quiz_card_shown, choice_rects, correct_answer = show_quiz_card(model, screen, font, preposition,
                                                                                   quiz_choices, quiz_card_surface)
            # user clicked a choice from the quiz card.
            elif event.type == pygame.MOUSEBUTTONDOWN and quiz_card_shown:
                # Check if the clicked position is within any of the choice rectangles
                preposition = board[clicked_cell[0]][clicked_cell[1]][0]
                for i, choice_rect in enumerate(choice_rects):
                    if choice_rect.collidepoint(event.pos):
                        # User selected a choice
                        selected_choice = quiz_choices[i]
                        # Check if the selected choice is correct
                        if selected_choice == board[clicked_cell[0]][clicked_cell[1]][0]:
                            # Correct answer, do something
                            print("Correct!")
                            # Hide the quiz card and update the game state accordingly
                            quiz_card_shown = False
                            correct_cell = clicked_cell
                            # Color the cell of the correctly answered quiz
                            board[correct_cell[0]][correct_cell[1]] = (
                                board[correct_cell[0]][correct_cell[1]][0], jellyfish_tiles[1],
                                GREEN)  # board[correct_cell[0]][correct_cell[1]][2])
                            if (check_win(board)):
                                print("You won")
                                game_over = True
                                game_state = "win"
                        else:
                            # Incorrect answer, do something
                            print("Incorrect!")
                            # Handle incorrect answer, e.g., show a message or deduct points
                            quiz_card_shown = False
                            incorrect_cell = clicked_cell
                            # Color the cell of the incorrectly answered quiz
                            board[incorrect_cell[0]][incorrect_cell[1]] = (
                                board[incorrect_cell[0]][incorrect_cell[1]][0], jellyfish_tiles[2], RED)
                            if (check_lose(board)):
                                print("You lose!")
                                game_over = True
                                game_state = "lost"

                if not quiz_card_shown:
                    screen.fill(WHITE)
                    draw_board(board, screen, background_image)
                if game_over:
                    if game_state == "win":
                        game_over_card(screen, WIN_MENU_IMG, font, GREEN, "لقد فزت!")
                    elif game_state == "lost":
                        game_over_card(screen, LOSE_MENU_IMG, font, RED, "حظاً أوفر")

        pygame.display.flip()
    pygame.quit()
