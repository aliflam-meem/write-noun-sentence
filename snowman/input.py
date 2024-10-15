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
        # Draw the input box
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))



#     # Example Pygame loop with the InputBox
#
#     # Initialize Pygame
# pygame.init()
#
# # Screen setup
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Input Box Example")
#
# # Colors
# WHITE = (255, 255, 255)
#
# # Create input box
# input_box = InputBox(400, 300, 200, 40)  # x, y, width, height
#
# # Game loop
# running = True
# while running:
#     screen.fill(WHITE)
#
#     # Event handling
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         input_box.handle_event(event)
#
#     # Update input box
#     input_box.update()
#
#     # Draw input box on the screen
#     input_box.draw(screen)
#
#     # Update the display
#     pygame.display.flip()
#
# pygame.quit()
