# Function to draw the title with background
import pygame

from snowman.constants import BUTTON_FONT_COLOR, SCREEN_WIDTH, TITLE_HEIGHT, DARK_GRAY, screen, title_font, \
    subtitle_font, saddlebrown


def draw_title(title, color= BUTTON_FONT_COLOR):
    title_background_rect = pygame.Rect(0, 0, SCREEN_WIDTH, TITLE_HEIGHT)
    pygame.draw.rect(screen, DARK_GRAY, title_background_rect)

    title_text = title_font.render(title, True, color)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, TITLE_HEIGHT // 2))
    screen.blit(title_text, title_rect)


def draw_subtitle(subtitle, x, y, color="white"):
    title_text = subtitle_font.render(subtitle, True, color)
    title_rect = title_text.get_rect()
    title_rect.topright = (x,y)
    screen.blit(title_text, title_rect)


def draw_button(text, x, y, width, height, border_width=2, border_color=saddlebrown, text_color = BUTTON_FONT_COLOR, highlight_color=brown, radius=10):
    """
    Draws a button with rounded corners.

    Args:
        text (str): The text to display on the button.
        x (int): The x-coordinate of the button's top-left corner.
        y (int): The y-coordinate of the button's top-left corner.
        width (int): The width of the button.
        height (int): The height of the button.
        border_width (int, optional): The width of the button's border. Defaults to 2.
        border_color (tuple, optional): The color of the button's border. Defaults to GRAY.
        highlight_color (tuple, optional): The color to use when the button is hovered over. Defaults to saddlebrown.
        radius (int, optional): The radius of the rounded corners. Defaults to 10.
    """

    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    # Draw border
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

    # Draw button text
    button_text = body_font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    return button_rect
