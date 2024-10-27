import inspect
import os
import sys

from src.core.utility import load_image


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.constants import RED, thumbnail_width, body_font, screen
from core.json_response_parser import *
from core.audio_player import *
from src.constants import  SCREEN_HEIGHT
from src.core.audio_player import *
from src.jar_bingo.LLM import *
from src.jar_bingo.board import *
from src.jar_bingo.game_over import *


# Function to show the quiz card
def show_quiz_card(model, screen, body_font, preposition, choices, quiz_card_surface):
    quiz_card_shown = True
    # Draw the resized quiz card image onto the screen
    quiz_card_image = pygame.image.load(QUIZ_IMG)
    # Resize the quiz card image to fit within the defined QUIZ_CARD_WIDTH and QUIZ_CARD_HEIGHT
    quiz_card_image = pygame.transform.scale(quiz_card_image, (QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT))
    screen.blit(quiz_card_image, (QUIZ_CARD_PADDING, QUIZ_CARD_PADDING + 20, QUIZ_CARD_WIDTH,
                                  QUIZ_CARD_HEIGHT))  # ((screen.get_width() - quiz_card_image.get_width()) // 2, (screen.get_height() - quiz_card_image.get_height()) // 2))
    pygame.draw.rect(screen, WHITE, (QUIZ_CARD_PADDING, QUIZ_CARD_PADDING + 20, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT), 4)
    # change to bring the qestions in bulk
    question_answer_pair = get_questions(model, preposition, 1, preposition, "")
    print("question_answer_pair", question_answer_pair)
    quiz_question = question_answer_pair.get("sentence")
    correct_answer = question_answer_pair.get("correct_answer")
    quiz_choices = choices
    # Adjust drawing positions based on the quiz card image content
    # question and choices
    text_margin = 20

    question_text = string_parser(quiz_question, F_Arial, BLACK)
    question_rect = question_text.get_rect(
        center=(quiz_card_image.get_width() // 2 + 100, 120 + (CHOICE_RECT_HEIGHT + CHOICE_RECT_PADDING)))
    screen.blit(question_text, question_rect)
    # Choice rects and text
    choice_rects = []
    for i, choice in enumerate(quiz_choices):
        choice_text = string_parser(choice, F_Arial, BLACK)
        # Adjust choice positioning based on margins and number of choices
        choice_y_position = quiz_card_image.get_height() // 2 + (i + 1) * (choice_text.get_height() // 2)
        choices_size = pygame.Rect(QUIZ_CARD_PADDING + 100, QUIZ_CARD_HEIGHT + (40 * i),
                                   QUIZ_CARD_WIDTH - 2 * QUIZ_CARD_PADDING, CHOICE_RECT_HEIGHT)
        choice_rect = choice_text.get_rect(center=(choices_size.left + choices_size.width // 2,
                                                   choices_size.top + choices_size.height // 2))  # choice_text.get_rect(center=(quiz_card_image.get_width() // 2, choice_y_position))
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


def load_jar_bingo_game_thumbnail():
    return load_image(jar_bingo_thumbnail, (thumbnail_width, thumbnail_width))


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
#def main():
def print_jarbingo_game_screen():
    # start game
    #clock = pygame.time.Clock()
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
                        game_over_card(screen, WIN_MENU_IMG, GREEN, True)
                    elif game_state == "lost":
                        game_over_card(screen, LOSE_MENU_IMG, RED, False)

        pygame.display.flip()