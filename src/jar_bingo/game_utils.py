import random

from src.core.utility import load_image, load_loading_image
from src.constants import thumbnail_width, body_font, screen
from src.core.json_response_parser import *
from src.core.audio_player import *
from src.core.audio_player import *
from src.jar_bingo.LLM import *
from src.jar_bingo.board import *
from src.jar_bingo.game_over import *


def check_cell_click(pos):
    """
    Check if the cell is clicked in the board, and return either the cell index. 

    """
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if i * CELL_SIZE < pos[0] < (i + 1) * CELL_SIZE and j * CELL_SIZE < pos[1] < (j + 1) * CELL_SIZE:
                return i, j
    return None

def prepare_board_prepositions_list(preposition, prep_parts_list):
    """
    Generate quiz_choices, two randomly generated prepositions -execluding from the list the correct choice-,
                and then added to them the correct choice.
    """
    if preposition in prepositions_single_letters and len(prep_parts_list)>1:
        print("prep_parts_list[1]", prep_parts_list[1])
        rest_of_prepositions = [element+prep_parts_list[1] for element in prepositions_single_letters if element != preposition]
        quiz_choices = [preposition] + random.sample(rest_of_prepositions, 2)
    else:
        rest_of_prepositions = [element for element in prepositions_2 if element != preposition]
        quiz_choices = [preposition] + random.sample(rest_of_prepositions, 2)
    return quiz_choices

def draw_quiz_card():
    """
    Draws the quiz card on screen, and returns the quiz card dim to center the rest of the content inside it.

    Args:
        None.
    """
    quiz_card_image = pygame.image.load(QUIZ_IMG)
    # Resize the quiz card image to fit within the defined QUIZ_CARD_WIDTH and QUIZ_CARD_HEIGHT
    quiz_card_image = pygame.transform.scale(quiz_card_image, (QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT))
    screen.blit(quiz_card_image, (QUIZ_CARD_PADDING, QUIZ_CARD_PADDING + 20, QUIZ_CARD_WIDTH,
                                    QUIZ_CARD_HEIGHT))  
    pygame.draw.rect(screen, WHITE, (QUIZ_CARD_PADDING, QUIZ_CARD_PADDING + 20, QUIZ_CARD_WIDTH, QUIZ_CARD_HEIGHT), 4)
    return quiz_card_image

def show_quiz_card_question(quiz_card_image, quiz_question):
    question_text = string_parser(quiz_question, body_font, BLACK, quiz_card_image.get_width())
    question_rect = question_text.get_rect(
        center=(quiz_card_image.get_width() // 2 + 100, 120 + (CHOICE_RECT_HEIGHT + CHOICE_RECT_PADDING)))
    screen.blit(question_text, question_rect)
    

def show_quiz_card_choices(quiz_choices):
    """
    Prints the quiz choices.

    Args:
        quiz_choices: Two randomly generated prepositions -execluding from the list the correct choice-,
                and then added to them the correct choice.
        
    Return:
        choice_rects : Choices list to tract which was clicked.
    """
    choice_rects = []
    for i, choice in enumerate(quiz_choices):
        choice_text = string_parser(choice, body_font, BLACK,0)
        # Adjust choice positioning based on margins and number of choices
        choices_size = pygame.Rect(QUIZ_CARD_PADDING + 100, QUIZ_CARD_HEIGHT + (40 * i),
                                   QUIZ_CARD_WIDTH - 2 * QUIZ_CARD_PADDING, CHOICE_RECT_HEIGHT)
        choice_rect = choice_text.get_rect(center=(choices_size.left + choices_size.width // 2,
                                                   choices_size.top + choices_size.height // 2))  
        pygame.draw.rect(screen, LIGHT_BLUE3, choices_size)  # choice fill
        pygame.draw.rect(screen, DARK_BLUE1, choices_size, 3)  # choice border

        screen.blit(choice_text, choice_rect)
        choice_rects.append(choice_rect)
    return choice_rects

def show_quiz_card(model, sexual_beh_and_racism_detection_model, quiz_card_shown, preposition):
    """
    Prints the quiz card and its questions and answers.

    Args:
        screen: The Pygame screen object.
        model: LLM model for generating quiz questions and answers.
        preposition: List of prepositions defined in the game.
    """
    #change the card state
    quiz_card_shown = True
    # Draw the resized quiz card image onto the screen
    quiz_card_image = draw_quiz_card()
    # change to bring the qestions in bulk
    #load_loading_image(text_message = "جار تحميل السؤال ...", text_color = WHITE, scale_x=100, scale_y=100)
    question_answer_pair, prep_parts_list = get_questions(model, "المبتدئ",preposition)
    print("question_answer_pair", question_answer_pair)
    quiz_question = question_answer_pair["sentence"] #currently supports 1 question
    correct_answer = question_answer_pair["correct_answer"]
    print("correct answer in func ", correct_answer)
    # Adjust drawing positions based on the quiz card image content
    # question
    show_quiz_card_question(quiz_card_image, quiz_question)
    # Choice rects and text
    quiz_choices = prepare_board_prepositions_list(correct_answer,prep_parts_list)
    choice_rects =  show_quiz_card_choices(quiz_choices)
    return quiz_card_shown, choice_rects, quiz_choices, correct_answer


def load_jar_bingo_game_thumbnail():
    """
    Loads game thumbnail.
    """
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