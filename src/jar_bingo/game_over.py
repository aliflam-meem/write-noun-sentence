import pygame

from src.constants import screen, body_font, YOU_WIN_AUDIO, YOU_LOST_AUDIO, IMAGE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT
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

    # Load the image
    image = pygame.image.load(image_path)

    # Scale the image to half the screen size
    image = pygame.transform.scale(image, (IMAGE_WIDTH, IMAGE_WIDTH))

    # Calculate the image position to center it
    x = (SCREEN_WIDTH - IMAGE_WIDTH) // 2
    y = (SCREEN_HEIGHT - IMAGE_WIDTH) // 1.5

    # Define the border size and color
    BORDER_SIZE = 10
    BORDER_COLOR = message_color  # Adjust to your preferred border color
    BORDER_RADIUS = 20  # Adjust the corner roundness here

    # Create a rounded rectangle for the border
    border_rect = pygame.Rect(x - BORDER_SIZE, y - BORDER_SIZE,
                                IMAGE_WIDTH + 2 * BORDER_SIZE, IMAGE_WIDTH + 2 * BORDER_SIZE)
    pygame.draw.rect(screen, BORDER_COLOR, border_rect, border_radius=BORDER_RADIUS)

    # Blit the image onto the screen
    screen.blit(image, (x, y))

    message = "أحسنت! لقد فُزت!!" if win_state else "لقد خسرت!"
    print("game over",message)
    
    message_text = body_font.render(message, True, message_color)
    # Calculate the message position to center it within the image
    message_x = x + (IMAGE_WIDTH - message_text.get_width()) // 2
    message_y = y + (IMAGE_WIDTH - message_text.get_height()) // 2
    # Blit the message onto the screen
    screen.blit(message_text, (message_x, message_y))

    # Blit the score
    score_message = f"{max_score}/{score}"
    score_message_text = body_font.render(message, True, message_color)
    height_score_padding = 50
    # Calculate the message position to center it within the image
    score_message_x = x + (IMAGE_WIDTH - score_message_text.get_width()) // 2 
    score_message_y = y + (IMAGE_WIDTH - score_message_text.get_height()) // 2 + height_score_padding
    # Blit the score_message onto the screen
    screen.blit(score_message_text, (score_message_x, score_message_y))

    #Play the audio
    audio = YOU_WIN_AUDIO if win_state else YOU_LOST_AUDIO
    print("play game over sounds.")
    play_sound(audio)
