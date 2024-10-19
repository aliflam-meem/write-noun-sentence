# Function to draw the title with background
import pygame

from constants import BUTTON_FONT_COLOR, SCREEN_WIDTH, TITLE_HEIGHT, DARK_GRAY, screen, title_font, \
    subtitle_font, saddlebrown, brown, body_font, BUTTON_COLOR, BUTTON_HEIGHT, BUTTON_WIDTH, LONG_PADDING, cornsilk, \
    HEALTH_POINT_IMAGE, numbering_font


def draw_title(title, title_height=TITLE_HEIGHT, color=BUTTON_FONT_COLOR):
    title_background_rect = pygame.Rect(0, 0, SCREEN_WIDTH, TITLE_HEIGHT)
    pygame.draw.rect(screen, DARK_GRAY, title_background_rect)

    title_text = title_font.render(title, True, color)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, title_height // 2))
    screen.blit(title_text, title_rect)


def draw_subtitle(subtitle, x, y, color="white"):
    title_text = subtitle_font.render(subtitle, True, color)
    title_rect = title_text.get_rect()
    title_rect.topright = (x, y)
    screen.blit(title_text, title_rect)


def draw_button(text, x, y, width, height, auto_width=False, border_width=2, border_color=saddlebrown,
                text_color=BUTTON_FONT_COLOR, highlight_color=brown, radius=10):
    """
    Draws a button with rounded corners.

    Args:
        text (str): The text to display on the button.
        x (int): The x-coordinate of the button's top-left corner.
        y (int): The y-coordinate of the button's top-left corner.
        width (int): The width of the button. If auto_width is True, this value is ignored.
        height (int): The height of the button.
        auto_width (bool, optional): If True, the button width is calculated based on the text length. Defaults to False.
        border_width (int, optional): The width of the button's border. Defaults to 2.
        border_color (tuple, optional): The color of the button's border. Defaults to saddlebrown.
        text_color (tuple, optional): The color of the button's text. Defaults to BUTTON_FONT_COLOR.
        highlight_color (tuple, optional): The color to use when the button is hovered over. Defaults to brown.
        radius (int, optional): The radius of the rounded corners. Defaults to 10.
    """

    # Render the button text
    button_text = body_font.render(text, True, text_color)
    text_rect = button_text.get_rect()

    # Automatically adjust the width based on the text if auto_width is True
    if auto_width:
        padding = 30  # Add padding around the text
        old_width = width
        width = text_rect.width + padding
        # calculate the new x coordinate based on the new width
        x = x + old_width - width

    # Create the button rectangle
    button_rect = pygame.Rect(x, y, width, height)

    # Get the mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Draw the button border
    pygame.draw.rect(screen, border_color, button_rect, border_width, border_radius=radius)

    # Change button color based on hover
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, highlight_color,
                         (x + border_width, y + border_width, width - 2 * border_width, height - 2 * border_width), 0,
                         border_radius=radius)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR,
                         (x + border_width, y + border_width, width - 2 * border_width, height - 2 * border_width), 0,
                         border_radius=radius)

    # Center the text in the button
    text_rect.center = button_rect.center
    screen.blit(button_text, text_rect)

    return button_rect


def draw_back_button():
    return draw_button("رجوع", 30, (TITLE_HEIGHT - BUTTON_HEIGHT) / 2, BUTTON_WIDTH - LONG_PADDING,
                       BUTTON_HEIGHT)


def draw_text_box(text, x, y, width, height, box_color=cornsilk, text_color=saddlebrown, add_border=False):
    # Create a rectangle for the input box
    input_box_rect = pygame.Rect(x, y, width, height)

    # Draw the input box rectangle
    pygame.draw.rect(screen, box_color, input_box_rect)

    # Draw the border around the input box
    if add_border:
        pygame.draw.rect(screen, "black", input_box_rect, 2)  # 2 is the border width

    # Render the input text inside the input box
    text_surface = body_font.render(text, True, text_color)

    # Calculate the position to align the text to the right
    text_width = text_surface.get_width()
    padding = 10  # You can adjust the padding as needed
    text_x = input_box_rect.right - text_width - padding  # Align text to the right with padding
    text_y = input_box_rect.y + padding  # Align the text vertically with padding

    # Blit the text surface on the input box (place the text inside the box)
    screen.blit(text_surface, (text_x, text_y))

    # Return the input box rectangle for further interactions (e.g., detecting clicks)
    return input_box_rect


def draw_image(image_path, x, y, width, height):
    # Load the image from the file
    image = pygame.image.load(image_path)

    # Resize the image to the specified width and height
    image = pygame.transform.scale(image, (width, height))

    # Blit (draw) the image at the specified (x, y) position on the screen
    screen.blit(image, (x, y))


def draw_score_and_health(score,x=30, y=30, health_points=2, max_score=100 , text_color=saddlebrown):
    """
    Draws the score and health points aligned to the left of the screen.

    Args:
        score (int): The current score.
        max_score (int): The maximum possible score.
        health_points (int): The number of remaining health points (hearts).
        x (int, optional): The x-coordinate of the score's top-left corner. Defaults to 30.
        y (int, optional): The y-coordinate of the score's top-left corner. Defaults to 30.

    """

    # The space between the score and the heart images.
    space_between = 25

    score_numbers_text = f"{max_score}/{score}"

    # Render the score text
    score_numbers_surface = numbering_font.render(score_numbers_text, True, text_color)

    # Get the width of the score text surface
    score_numbers_rect = score_numbers_surface.get_rect(topleft=(x, y))

    # Draw the score text on the screen
    screen.blit(score_numbers_surface, score_numbers_rect)

    score_text = "النقاط: "
    score_surface = body_font.render(score_text, True, text_color)
    score_rect = score_surface.get_rect(topleft=(score_numbers_rect.x + score_numbers_rect.width, y))
    screen.blit(score_surface, score_rect)

    # Scale the heart image to the desired size
    heart_width = 35
    # 13 is magic number
    heart_height = score_rect.height - 13
    scaled_heart = pygame.transform.scale(HEALTH_POINT_IMAGE, (heart_width, heart_height))

    # Calculate the x-coordinate for the hearts (next to the score)
    heart_x = score_rect.right + space_between
    heart_y = y + 5

    # Draw the hearts based on the health_points value
    for i in range(health_points):
        heart_rect = pygame.Rect(heart_x + i * (heart_width + 10), heart_y, heart_width, heart_height)
        screen.blit(scaled_heart, heart_rect)