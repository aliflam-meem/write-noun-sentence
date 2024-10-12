import pygame
import math


# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Ladder Rungs")

# Define Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)  # Color for the ladder

# Clock to control the frame rate
clock = pygame.time.Clock()


# Helper function to draw a thick line using polygons
def draw_thick_line(screen, color, start_pos, end_pos, thickness):
    """
    Draws a thick line by creating a polygon representing the width of the line.

    :param screen: The Pygame surface to draw on.
    :param color: The color of the line.
    :param start_pos: Starting (x, y) coordinates of the line.
    :param end_pos: Ending (x, y) coordinates of the line.
    :param thickness: The thickness of the line.
    """
    # Calculate the vector perpendicular to the line
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    length = math.sqrt(dx ** 2 + dy ** 2)

    # Unit vector perpendicular to the line direction
    perp_dx = -dy / length * thickness / 2
    perp_dy = dx / length * thickness / 2

    # Four points of the polygon representing the thick line
    points = [
        (start_pos[0] + perp_dx, start_pos[1] + perp_dy),
        (start_pos[0] - perp_dx, start_pos[1] - perp_dy),
        (end_pos[0] - perp_dx, end_pos[1] - perp_dy),
        (end_pos[0] + perp_dx, end_pos[1] + perp_dy)
    ]

    # Draw the polygon
    pygame.draw.polygon(screen, color, points)


# Ladder Drawing Function
def draw_ladder(screen, top_left, bottom_left, ladder_width, rung_spacing_percentage):
    """
    Draws a rotated ladder with dynamically spaced rungs based on ladder height.

    :param screen: The Pygame screen to draw on.
    :param top_left: The (x, y) coordinates of the top-left corner of the ladder.
    :param bottom_left: The (x, y) coordinates of the bottom-left corner of the ladder.
    :param ladder_width: The width of the ladder.
    :param rung_spacing_percentage: The spacing between the rungs as a percentage of the ladder height.
    """
    rail_thickness = 7  # Thickness of the vertical rails
    rung_thickness = 6  # Thickness of the rungs
    bottom_margin_percentage = 10  # Margin from the bottom to avoid rungs at the very bottom

    # Calculate the height of the ladder
    ladder_height = math.sqrt((bottom_left[0] - top_left[0]) ** 2 + (bottom_left[1] - top_left[1]) ** 2)

    # Calculate the angle of rotation (in radians) between the two points
    angle = math.atan2(bottom_left[1] - top_left[1], bottom_left[0] - top_left[0])

    # Offset for the right rail (perpendicular to the ladder direction)
    dx = ladder_width * math.sin(angle)
    dy = ladder_width * math.cos(angle)

    # Coordinates for the left and right rails (rotated)
    left_rail_top = top_left
    right_rail_top = (top_left[0] + dx, top_left[1] - dy)
    left_rail_bottom = bottom_left
    right_rail_bottom = (bottom_left[0] + dx, bottom_left[1] - dy)

    # Draw the two vertical rails using the thick line function
    draw_thick_line(screen, BROWN, left_rail_top, left_rail_bottom, rail_thickness)
    draw_thick_line(screen, BROWN, right_rail_top, right_rail_bottom, rail_thickness)

    # Calculate rung spacing based on ladder height
    rung_spacing = ladder_height * (rung_spacing_percentage / 100)

    # Draw the rungs dynamically based on the ladder height
    current_height = rung_spacing
    max_rung_height = ladder_height * (1 - bottom_margin_percentage / 100)  # Leave a margin at the bottom
    while current_height < max_rung_height:
        rung_pos = (
            top_left[0] + current_height * math.cos(angle),  # X position of the rung
            top_left[1] + current_height * math.sin(angle)  # Y position of the rung
        )

        # Draw the rungs as thick lines between the two rails
        rung_start = (rung_pos[0], rung_pos[1])
        rung_end = (rung_pos[0] + dx, rung_pos[1] - dy)
        draw_thick_line(screen, BROWN, rung_start, rung_end, rung_thickness)

        current_height += rung_spacing  # Move to the next rung


# Main loop
def game_loop():
    running = True
    while running:
        SCREEN.fill(WHITE)  # Clear the screen with a white background

        # Define the top-left and bottom-left corners of the ladder
        top_left = (150, 50)  # x, y coordinates of the top-left point
        bottom_left = (100, 350)  # x, y coordinates of the bottom-left point

        # Define the width of the ladder and the spacing percentage for the rungs
        ladder_width = 80
        rung_spacing_percentage = 10  # Rungs will be spaced at every 10% of the ladder height

        # Draw the ladder based on the two points
        draw_ladder(SCREEN, top_left, bottom_left, ladder_width, rung_spacing_percentage)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the display
        pygame.display.update()

        # Frame rate
        clock.tick(30)

    pygame.quit()


# Run the game loop
game_loop()
