import pygame

from constants import body_font, screen


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = "black"
        self.text = text
        self.font = body_font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def y(self, y):
        self.rect.y = y

    def x(self, x):
        self.rect.x = x

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("down")
            # Always set active to True when clicked
            if self.rect.collidepoint(event.pos):

                self.active = True  # Always activate on click
            else:
                self.active = False

            # Change the color based on active state
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Handle text submission here
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Remove last character
                else:
                    self.text += event.unicode  # Add new character to the text

                # Re-render the text
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self):
        # Calculate the position to align the text to the right
        text_width = self.txt_surface.get_width()
        padding = 10  # You can adjust the padding as needed
        text_x = self.rect.right - text_width - padding  # Align text to the right with padding
        text_y = self.rect.y + padding  # Align the text vertically with padding

        # Blit the text surface on the input box (place the text inside the box)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (text_x, text_y))
