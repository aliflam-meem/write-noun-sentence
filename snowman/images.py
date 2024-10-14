import pygame
import sys


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
IMAGE_WIDTH = 200
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
FONT_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
BUTTON_COLOR = (70, 130, 180)

# Create the Pygame screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Image Viewer with Button")

# Load fonts
arabic_font = pygame.font.Font("Arial.ttf", FONT_SIZE)  # 30 is font size
arabic_font.set_script("Arab")
arabic_font.set_direction(pygame.DIRECTION_RTL)

# Load images (You would load your own image files here)
# For demonstration purposes, let's assume we have 5 images loaded
# Replace the "image_path" with actual image paths
images = [
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT/2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT/2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT/2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT/2)),  # Placeholder surface as an image
    pygame.Surface((IMAGE_WIDTH, SCREEN_HEIGHT/2))  # Placeholder surface as an image
]

# Fill the placeholder surfaces with different colors to simulate different images
images[0].fill((255, 0, 0))  # Red image
images[1].fill((0, 255, 0))  # Green image
images[2].fill((0, 0, 255))  # Blue image
images[3].fill((255, 255, 0))  # Yellow image
images[4].fill((255, 0, 255))  # Magenta image

current_image_index = 0  # Start by displaying the first image

# Function to draw the button
def draw_button(text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    # Change color on hover
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, LIGHT_GRAY, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

    # Render button text
    button_text = arabic_font.render(text, True, "white")
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    return button_rect


# Function to display the current image
def display_image(index):
    image = images[index]
    screen.blit(image, (50, 100))  # Display image on the left (at 0, 0)


# Main game loop
def main():
    global current_image_index
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)  # Set background color of the screen

        # Display the current image on the left
        display_image(current_image_index)

        # Draw the button on the right
        button_rect = draw_button("أجب", SCREEN_WIDTH - BUTTON_WIDTH - 20,
                                  SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if button_rect.collidepoint(event.pos):
                    # Cycle to the next image
                    current_image_index = (current_image_index + 1) % len(images)
                    print(f"Current image index: {current_image_index}")

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
