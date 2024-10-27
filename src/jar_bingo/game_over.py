import pygame

from src.constants import screen, body_font, YOU_WIN_AUDIO, YOU_LOST_AUDIO, IMAGE_WIDTH
from src.core.audio_player import play_sound


def game_over_card(image_path, message_color, win_state, score, max_score):
    """
    Prints the game over scene on top of the board, centered horizontally and vertically.

    Args:
        image_path: The path to the image file.
        message_color: The color of the message text.
        win_state: win (True) or lose (False).
        score: Player's score at the end of the game.
        max_score : to display it as the base score.

    """
    message = "أحسنت! لقد فُزت!!" if win_state else "لقد خسرت!"
    message = message + "\n" + f"{max_score}/{score}"

    # Load the image
    image = pygame.image.load(image_path)

    # Scale the image to half the screen size
    image = pygame.transform.scale(image, (IMAGE_WIDTH, IMAGE_WIDTH))

    # Calculate the image position to center it
    # x = (SCREEN_WIDTH - IMAGE_WIDTH) // 2
    # y = (SCREEN_HEIGHT - IMAGE_WIDTH) // 1.5

    x = 10
    y = 10

    # Blit the image onto the screen
    screen.blit(image, (x, y))

    message_text = body_font.render(message, True, message_color)
    # Calculate the message position to center it within the image
    message_x = x + (IMAGE_WIDTH - message_text.get_width()) // 2
    message_y = y + (IMAGE_WIDTH - message_text.get_height()) // 2

    # Blit the message onto the screen
    screen.blit(message_text, (message_x, message_y))
    audio = YOU_WIN_AUDIO if win_state else YOU_LOST_AUDIO
    play_sound(audio)
