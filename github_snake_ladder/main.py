import pygame
import random
import math


display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake And Ladder')

clock = pygame.time.Clock()

# some Variables
crashed = False
pause = True
size = 25
roll = False
DONE1 = False
cell_size = 60
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)  # Color for the ladder

# colors used
back = (96, 107, 114)
forg = (255, 138, 119)
darkback = (53, 53, 53)
boardclr = (255, 199, 95)
boardclr2 = (255, 237, 203)
snkclr = (168, 187, 92)
ladclr = (195, 64, 54)
pla1clr = (0, 211, 255)
pla2clr = (255, 121, 191)

color_palette_snake = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 90) for i in range(8)]


# after Win
def WINNER():
    pygame.draw.rect(gameDisplay, (back), (95, 95, 610, 410))
    pygame.draw.rect(gameDisplay, (darkback), (100, 100, 600, 400))
    pygame.draw.rect(gameDisplay, (back), (105, 105, 590, 390))
    smallText = pygame.font.SysFont("comicsansms", 90)
    textSurf, textRect = text_objects("GAME OVER", smallText, darkback)
    textRect.center = ((display_width // 2), (display_height // 2 - 100))
    gameDisplay.blit(textSurf, textRect)

    smallText = pygame.font.SysFont("comicsansms", 50)
    textSurf, textRect = text_objects("WINNER : ", smallText, darkback)
    textRect.center = ((display_width // 4 + 100), (display_height // 2 + 100))
    gameDisplay.blit(textSurf, textRect)

    smallText1 = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects("Hit Space to Play", smallText1, darkback)
    textRect.center = ((700), (580))
    gameDisplay.blit(textSurf, textRect)

    if turn == 1:
        pygame.draw.circle(gameDisplay, pla2.clr, ((3 * display_width // 4), (display_height // 2 + 100)), cell_size)
    elif turn == 2:
        pygame.draw.circle(gameDisplay, pla1.clr, ((3 * display_width // 4), (display_height // 2 + 100)), cell_size)
    temp = True
    while temp:
        global crashed, DONE1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                temp = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    global b
                    gameDisplay.fill(back)
                    b.__init__()
                    pla1.__init__(b, pla1clr)
                    pla2.__init__(b, pla2clr)
                    temp = False
                    DONE1 = False
        pygame.display.update()


# def draw_cartoon_snake(start_pos, end_pos, color):
#     # Calculate the direction of the snake
#     dx = end_pos[0] - start_pos[0]
#     dy = end_pos[1] - start_pos[1]
#     angle = math.atan2(dy, dx)
#
#     # Draw the snake's head
#     head_x = start_pos[0] + 20 * math.cos(angle)
#     head_y = start_pos[1] + 20 * math.sin(angle)
#     pygame.draw.ellipse(gameDisplay, color, (head_x - 15, head_y - 15, 30, 30))
#
#     # Draw the snake's eyes
#     eye_radius = 5
#     eye_x = head_x + 5
#     eye_y = head_y - 5
#     pygame.draw.circle(gameDisplay, (0, 0, 0), (eye_x, eye_y), eye_radius)
#     pygame.draw.circle(gameDisplay, (255, 255, 255), (eye_x + eye_radius // 2, eye_y + eye_radius // 2), eye_radius // 2)
#
#     # Draw the snake's tongue
#     tongue_length = 10
#     tongue_x = head_x + 25 * math.cos(angle)
#     tongue_y = head_y + 25 * math.sin(angle)
#     pygame.draw.line(gameDisplay, (255, 0, 0), (tongue_x, tongue_y), (tongue_x + tongue_length * math.cos(angle + math.pi / 4), tongue_y + tongue_length * math.sin(angle + math.pi / 4)), 2)
#
#     # Draw the snake's body
#     body_length = int(math.sqrt(dx**2 + dy**2)) - 40  # Adjust length as needed
#     body_segments = 5  # Adjust number of segments
#     segment_length = body_length // body_segments
#     for i in range(1, body_segments + 1):
#         x = start_pos[0] + i * segment_length * math.cos(angle)
#         y = start_pos[1] + i * segment_length * math.sin(angle)
#         pygame.draw.rect(gameDisplay, color, (x - 10, y - 10, 20, 20))

class Snake:

    def __init__(self, start_pos, end_pos, color, num_turns=2, amplitude=80, body_radius=8, head_radius=16,
                 num_points_per_segment=40):
        """
        Initializes the Snake object.
        :param start_pos: Tuple representing the starting (head) position of the snake.
        :param end_pos: Tuple representing the ending (tail) position of the snake.
        :param num_turns: Number of turns the snake should make.
        :param amplitude: Height of the turns (vertical distance of the curves).
        :param body_radius: Radius of the snake's body segments.
        :param head_radius: Radius of the snake's head.
        :param num_points_per_segment: Number of interpolated points between control points.
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.num_turns = num_turns
        self.amplitude = amplitude
        self.body_radius = body_radius
        self.head_radius = head_radius
        self.num_points_per_segment = num_points_per_segment
        self.color = color

        # Generate the control points dynamically based on the number of turns
        self.control_points = self.generate_control_points()

    def generate_control_points(self):
        """
        Generates control points to create the desired number of turns between the start and end points.
        The control points will alternate between upward and downward curves, forming sinusoidal turns.
        """
        control_points = []

        # Horizontal distance between start and end
        x_distance = self.end_pos[0] - self.start_pos[0]

        # Generate control points in an alternating up and down pattern
        for i in range(self.num_turns * 2 + 1):
            # Interpolate the x position based on the number of turns
            x = self.start_pos[0] + i * (x_distance / (self.num_turns * 2))

            # Alternate the y position between upwards (+amplitude) and downwards (-amplitude)
            if i % 2 == 0:
                y = self.start_pos[1]  # Keep even-indexed points on the middle line
            else:
                # Create upward or downward curves by alternating between positive and negative amplitudes
                y = self.start_pos[1] + (-1) ** (i // 2) * self.amplitude

            control_points.append((x, y))

        # Ensure the last control point is at the specified end position
        control_points[-1] = self.end_pos

        return control_points

    def catmull_rom_spline(self, P0, P1, P2, P3):
        """
        Given four control points, this function returns points along the
        Catmull-Rom spline that passes through the middle two points.
        """
        points = []
        for t in range(self.num_points_per_segment):
            t = t / self.num_points_per_segment
            t2 = t * t
            t3 = t2 * t
            f0 = -0.5 * t3 + t2 - 0.5 * t
            f1 = 1.5 * t3 - 2.5 * t2 + 1.0
            f2 = -1.5 * t3 + 2.0 * t2 + 0.5 * t
            f3 = 0.5 * t3 - 0.5 * t2

            x = f0 * P0[0] + f1 * P1[0] + f2 * P2[0] + f3 * P3[0]
            y = f0 * P0[1] + f1 * P1[1] + f2 * P2[1] + f3 * P3[1]

            points.append((x, y))
        return points

    def draw_ellipse_head(self, screen, head_pos, angle):
        """
        Draws the snake's head as an ellipse with eyes, rotated based on the given angle.
        :param screen: Pygame screen surface to draw on.
        :param head_pos: The (x, y) position of the snake's head.
        :param angle: The angle at which the ellipse should be rotated to align with the snake's body.
        """
        x, y = int(head_pos[0]), int(head_pos[1])
        ellipse_width = self.head_radius * 1.5
        ellipse_height = self.head_radius

        # Create a surface for the head to rotate it
        head_surface = pygame.Surface((ellipse_width * 2, ellipse_height * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(head_surface, self.color, (0, 0, ellipse_width * 2, ellipse_height * 2))

        # Rotate the surface
        rotated_head = pygame.transform.rotate(head_surface, -math.degrees(angle))

        # Position the rotated head
        head_rect = rotated_head.get_rect(center=(x, y))
        screen.blit(rotated_head, head_rect)

        # Draw eyes as small circles
        eye_radius = 3
        eye_offset_x = ellipse_width / 4  # Horizontal offset for the eyes
        eye_offset_y = ellipse_height / 4  # Vertical offset for the eyes

        left_eye_pos = (x - eye_offset_x, y - eye_offset_y)
        right_eye_pos = (x + eye_offset_x, y - eye_offset_y)

        pygame.draw.circle(screen, BLACK, left_eye_pos, eye_radius)
        pygame.draw.circle(screen, BLACK, right_eye_pos, eye_radius)

    def draw(self, screen):
        """
        Draws the snake on the screen by interpolating between control points.
        :param screen: Pygame screen surface to draw on.
        """

        P0, P1, P2, P3 = self.control_points[:4]
        snake_points = self.catmull_rom_spline(P0, P1, P2, P3)

        # Loop through control points and draw the snake segments using curves
        for i in range(len(self.control_points) - 3):
            P0, P1, P2, P3 = self.control_points[i], self.control_points[i + 1], self.control_points[i + 2], \
                             self.control_points[i + 3]
            snake_points = self.catmull_rom_spline(P0, P1, P2, P3)

            # Draw the snake body by placing circles at interpolated points
            self.draw_snake_body(screen, snake_points)

        self.draw_snake_head(screen, snake_points[-1], snake_points[-2])

    def draw_snake_body(self, screen, points):
        for point in points:
            circle_surface = pygame.Surface((self.body_radius*2, self.body_radius *2), pygame.SRCALPHA)  # Create a surface with alpha
            pygame.draw.circle(circle_surface, self.color,
                               (self.body_radius, self.body_radius), self.body_radius)  # Draw semi-transparent circle
            screen.blit(circle_surface, (int(point[0]) - self.body_radius, int(point[1]) - self.body_radius))

    def draw_snake_head(self, screen, head_pos, prev_pos):
        angle = math.atan2(head_pos[1] - prev_pos[1], head_pos[0] - prev_pos[0])
        # Draw the snake head as an ellipse
        self.draw_ellipse_head(screen, head_pos, angle)


# game Board Class
class Board:
    def __init__(self):
        # Board List (Reversed order)
        self.boardarr = []
        count = 100

        # Load the three textures
        self.textures = [
            pygame.image.load('grass_surface_dark.png'),
            pygame.image.load('grass_surface_light.png'),
        ]

        # Generate 2D Board  10 X 10
        for i in range(0, 10):
            temp = []
            for j in reversed(range(0, 10)):  # Iterate in reverse for bottom-right numbering
                x = j * cell_size
                y = i * cell_size
                temp.append((x, y, count))
                count -= 1
            self.boardarr.append(temp)

        # Generate Random Ladders
        self.ladders = []
        self.countarr = [100, 1]
        num_of_ladders = random.randint(4, 6)
        for i in range(num_of_ladders):
            val = True
            while val:
                rand1 = random.randint(1, 100)
                rand2 = random.randint(1, 100)
                diff = rand2 - rand1  # Reverse order for bottom-right numbering
                if diff > 10 or diff < -10:
                    if rand1 not in self.countarr and rand2 not in self.countarr:
                        val = False
                        self.countarr.append(rand1)
                        self.countarr.append(rand2)
            a = None
            b = None
            for x in self.boardarr:
                for y in x:
                    if rand2 == y[2]:  # Use rand2 for bottom-right numbering
                        a = y
                    if rand1 == y[2]:
                        b = y
            self.ladders.append((a, b))

        # Generate Random Snakes
        num_of_snakes = random.randint(4, 6)
        self.snakes = []
        for i in range(num_of_snakes):
            val = True
            while val:
                rand1 = random.randint(1, 100)
                rand2 = random.randint(1, 100)
                diff = rand2 - rand1  # Reverse order for bottom-right numbering
                if diff > 10 or diff < -10:
                    if rand1 not in self.countarr and rand2 not in self.countarr:
                        val = False
                        self.countarr.append(rand1)
                        self.countarr.append(rand2)
            a = None
            b = None
            for x in self.boardarr:
                for y in x:
                    if rand2 == y[2]:  # Use rand2 for bottom-right numbering
                        a = y
                    if rand1 == y[2]:
                        b = y
            self.snakes.append((a, b))


    def validate_position(self, p):
        if p[0] >= display_width - cell_size:
            p[0] = display_width - cell_size * 2
        elif p[0] <= cell_size:
            p[0] = cell_size * 2
        if p[1] >= display_height - cell_size:
            p[1] = display_height - cell_size * 2
        elif p[1] <= cell_size:
            p[1] = cell_size * 2

    def draw(self):
        for i, row in enumerate(self.boardarr):
            for j, cell in enumerate(row):
                # Calculate adjusted position for rounded rect or custom shape
                x, y = cell[0], cell[1]

                # Pick one of the three textures based on the cell's position (e.g., alternating or random)
                texture_index = (i + j) % len(self.textures)  # Alternates textures based on row and column
                chosen_texture = self.textures[texture_index]

                # Draw rounded rectangle with the chosen texture overlay
                textured_rect = pygame.Surface((59, 59), pygame.SRCALPHA)  # Adjust for texture size
                textured_rect.blit(chosen_texture, (0, 0), (0, 0, cell_size, cell_size))
                gameDisplay.blit(textured_rect, (x, y))

                # Enhance text rendering
                smallText = pygame.font.SysFont("fantasyfont.ttf", 25)
                textSurf, textRect = text_objects(str(cell[2]), smallText, (255, 255, 255))
                textRect.center = ((x + (59 // 2)), (y + (59 // 2)))

                # Draw the actual text
                gameDisplay.blit(textSurf, textRect)

            counter = 0
            for x in self.snakes:
                start_pos = [x[0][0] + 30, x[0][1] + 30]
                end_pos = [x[1][0] + 30, x[1][1] + 30]
                self.validate_position(start_pos)
                self.validate_position(end_pos)
                snake = Snake(start_pos, end_pos, color_palette_snake[counter])
                snake.draw(gameDisplay)
                counter += 1

            for x in self.ladders:
                start_pos = [x[0][0] + cell_size/3, x[0][1] + cell_size/2]
                end_pos = [x[1][0] + cell_size/3, x[1][1] + cell_size/2]
                self.validate_position(start_pos)
                self.validate_position(end_pos)
                draw_ladder(gameDisplay, start_pos, end_pos)


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
def draw_ladder(screen, top_left, bottom_left, ladder_width=cell_size/2, rung_spacing_percentage=cell_size/3):
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

# Player class
class Player:

    def __init__(self, B, clr):
        self.val = 1  # Start at position 1
        self.xpos = None
        self.ypos = None
        self.barr = B.boardarr
        self.lad = B.ladders
        self.snk = B.snakes
        self.clr = clr
        self.size = random.randint(15, 25)
        for x in self.barr:
            for y in x:
                if self.val == y[2]:
                    a = y
                    self.xpos = y[0]
                    self.ypos = y[1]

    def move(self, no):
        # Limit the move to not exceed 100
        new_val = min(self.val + no, 100)
        if new_val > self.val:
            self.val = new_val
        else:
            print("You can't move that many spaces.")

        # Check for win
        if self.val == 100:
            print("+=+" * 10 + " YOU WIN " + "+=+" * 10)
            global DONE1
            DONE1 = True

        # Update position based on new value
        for x in self.barr:
            for y in x:
                if self.val == y[2]:
                    self.xpos = y[0]
                    self.ypos = y[1]

        # Handle ladders and snakes
        for l in self.lad:
            if (self.ypos == l[0][1] and self.xpos == l[0][0]) or (self.ypos == l[1][1] and self.xpos == l[1][0]):
                # Check if you landed on the higher end of the ladder (use min for bottom-right numbering)
                if self.val == min(l[0][2], l[1][2]):
                    self.val = max(l[0][2], l[1][2])
                    # Update position based on new value
                    for x in self.barr:
                        for y in x:
                            if self.val == y[2]:
                                self.xpos = y[0]
                                self.ypos = y[1]

        for l in self.snk:
            if (self.ypos == l[0][1] and self.xpos == l[0][0]) or (self.ypos == l[1][1] and self.xpos == l[1][0]):
                # Check if you landed on the lower end of the snake (use max for bottom-right numbering)
                if self.val == max(l[0][2], l[1][2]):
                    self.val = min(l[0][2], l[1][2])
                    # Update position based on new value
                    for x in self.barr:
                        for y in x:
                            if self.val == y[2]:
                                self.xpos = y[0]
                                self.ypos = y[1]

    def draw(self):
        pygame.draw.circle(gameDisplay, (self.clr), (self.xpos + 30, self.ypos + 30), self.size)


def text_objects(text, font, clr, *kward):
    if len(kward) > 0:
        textSurface = font.render(text, True, clr, kward[0])
    else:
        textSurface = font.render(text, True, clr)
    return textSurface, textSurface.get_rect()


# functions for dice
def one():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 2)), (y + (h // 2))), size)


def two():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 2))), size)


def three():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 2)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4))), size)


def four():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (3 * h // 4))), size)


def five():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 2)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (3 * h // 4))), size)


def six():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 2))), size)

    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 4)) - 10), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4)) + 10), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4)) - 10), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (3 * h // 4)) + 10), size)


# pygame Start

pygame.init()

b = Board()
pla1 = Player(b, (0, 211, 255))
pla2 = Player(b, (255, 121, 191))
turn = 1
gameDisplay.fill(back)
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if roll == True:
                    roll = False
                else:
                    roll = True

    if not DONE1:
        b.draw()
        pla1.draw()
        pla2.draw()
        smallText = pygame.font.SysFont("comicsansms", 40)
        textSurf, textRect = text_objects(str("Turn"), smallText, darkback, back)
        textRect.center = ((700), (300))
        gameDisplay.blit(textSurf, textRect)
        smallText1 = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects("Hit Space to Play", smallText1, darkback, back)
        textRect.center = ((700), (500))
        gameDisplay.blit(textSurf, textRect)
        if roll:
            time = random.randint(5, 25)
            for i in range(time):
                no = random.randint(1, 6)
                if no == 1:
                    one()
                elif no == 2:
                    two()
                elif no == 3:
                    three()
                elif no == 4:
                    four()
                elif no == 5:
                    five()
                elif no == 6:
                    six()
                pygame.time.wait(100)
                pygame.display.update()

            roll = False
            if turn == 1:
                pla1.move(no)
                turn = 2
                pygame.draw.circle(gameDisplay, pla2.clr, (700, 400), 50)
            elif turn == 2:
                pla2.move(no)
                turn = 1
                pygame.draw.circle(gameDisplay, pla1.clr, (700, 400), 50)
    else:
        WINNER()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()
