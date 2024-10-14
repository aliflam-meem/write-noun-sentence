import pygame


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Display 2D OBJ in Pygame")


def load_obj(file_path):
    """ Simple OBJ file loader for 2D vertices and faces. """
    vertices = []
    faces = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == 'v':  # Vertex definition
                # Store only the X, Y coordinates (assuming Z is not needed for 2D)
                vertices.append([float(parts[1]), float(parts[2])])
            elif parts[0] == 'f':  # Face definition (triangular faces)
                face = [int(idx.split('/')[0]) - 1 for idx in parts[1:]]  # Convert to 0-indexed
                faces.append(face)
    return vertices, faces


def draw_object(screen, vertices, faces):
    """ Draw the 2D object by rendering its faces as polygons. """
    for face in faces:
        points = []
        for vertex_index in face:
            vertex = vertices[vertex_index]
            points.append((vertex[0] * 100 + 400, vertex[1] * 100 + 300))  # Scale and center on screen

        # Draw the face as a filled polygon
        pygame.draw.polygon(screen, (0, 255, 0), points, 1)  # Green wireframe


# Load the OBJ file (assuming it's 2D)
vertices, faces = load_obj('snake.obj')  # Make sure 'snake.obj' is in the same directory

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen with black
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the 2D snake model
    draw_object(screen, vertices, faces)

    # Update the display
    pygame.display.flip()

pygame.quit()
