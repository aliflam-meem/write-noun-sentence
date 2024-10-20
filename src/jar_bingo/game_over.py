import pygame
from settings import *
from src.core.play_audio import play_sound

def game_over_card(screen, image_path, message_font, message_color, message, audio_var):
    """
    Prints a message on top of the board, centered horizontally and vertically.

    Args:
        screen: The Pygame screen object.
        image_path: The path to the image file.
        message_font: The font object for the message.
        message_color: The color of the message text.
    """

    # Load the image
    image = pygame.image.load(image_path)

    # Scale the image to half the screen size
    image = pygame.transform.scale(image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Calculate the image position to center it
    x = (SCREEN_WIDTH - image.get_width()) // 2
    y = (SCREEN_HEIGHT - image.get_height()) // 1.5

    # Blit the image onto the screen
    screen.blit(image, (x, y))

    # Create the "You win!" message
    message_font = pygame.font.Font(F_Arial, 35)
    message_font.set_script("Arab")
    message_font.set_direction(pygame.DIRECTION_RTL)
    message_text = message_font.render(message, True, message_color)
    # Calculate the message position to center it within the image
    message_x = x + (image.get_width() - message_text.get_width()) // 2
    message_y = y + (image.get_height() - message_text.get_height()) // 2

    # Blit the message onto the screen
    screen.blit(message_text, (message_x, message_y))
    play_sound(WIN_1)
