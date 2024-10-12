import pygame
import random
import sys


# VARIABLES

# Player 1

player_1_points = 0
player_1_x = 0
player_1_y = 295
player_1_square = pygame.Rect(player_1_x, player_1_y, 27, 32)

# Player 2

player_2_points = 0
player_2_x = 0
player_2_y = 295
player_2_square = pygame.Rect(player_2_x, player_2_y, 27, 32)

# Player 3

player_3_points = 0
player_3_x = 0
player_3_y = 295
player_3_square = pygame.Rect(player_3_x, player_3_y, 27, 32)

# Player 4

player_4_points = 0
player_4_x = 0
player_4_y = 295
player_4_square = pygame.Rect(player_4_x, player_4_y, 27, 37)


# TOKEN

def tokens(player_1_x, player_1_y, player_2_x, player_2_y, player_3_x, player_3_y, player_4_x, player_4_y,
           player_1_square, player_2_square, player_3_square, player_4_square):
    pygame.draw.rect(background, (150, 0, 150), player_1_square)
    pygame.draw.rect(background, (150, 150, 150), player_2_square)
    pygame.draw.rect(background, (194, 164, 31), player_3_square)
    pygame.draw.rect(background, (255, 0, 0), player_4_square)


# MOVEMENT


def move_left(x):
    x -= 1
    tokens(player_1_x, player_1_y, player_2_x, player_2_y, player_3_x, player_3_y, player_4_x, player_4_y,
           player_1_square, player_2_square, player_3_square, player_4_square)
    return (x)


def move_right(x):
    x += 1
    tokens(player_1_x, player_1_y, player_2_x, player_2_y, player_3_x, player_3_y, player_4_x, player_4_y,
           player_1_square, player_2_square, player_3_square, player_4_square)
    return (x)


def move_up(y):
    y -= 1
    tokens(player_1_x, player_1_y, player_2_x, player_2_y, player_3_x, player_3_y, player_4_x, player_4_y,
           player_1_square, player_2_square, player_3_square, player_4_square)
    return (y)


def move_down(y):
    y += 1
    tokens(player_1_x, player_1_y, player_2_x, player_2_y, player_3_x, player_3_y, player_4_x, player_4_y,
           player_1_square, player_2_square, player_3_square, player_4_square)
    return (y)


def player_1_turn(p1p, p1x, p1y):
    p1r = p1p // 10
    p1c = p1r % 10

    dice = random.randint(1, 6)

    p1p += dice

    new_p1r = p1p // 10
    new_p1c = p1p % 10

    if new_p1r > p1r:
        for x in range(48):
            move_up(p1y)
        for x in range(36 * (p1c - new_p1c)):
            move_left(p1x)
    else:
        for x in range(36 * (new_p1c - p1c)):
            move_right(p1x)

    ladder_check(p1p, p1x, p1y)
    snake_check(p1p, p1x, p1y)
    end_check(p1p)
    return p1p, p1x, p1y


def player_2_turn(p2p, p2x, p2y):
    p2r = p2p // 10
    p2c = p2r % 10

    dice = random.randint(1, 6)

    p2p += dice

    new_p2r = p2p // 10
    new_p2c = p2p % 10

    if new_p2r > p2r:
        for x in range(48):
            move_up(p2y)
        for x in range(36 * (p2c - new_p2c)):
            move_left(p2x)
    else:
        for x in range(36 * (new_p2c - p2c)):
            move_right(p2x)

    ladder_check(p2p, p2x, p2y)
    snake_check(p2p, p2x, p2y)
    end_check(p2p)
    return p2p, p2x, p2y


def player_3_turn(p3p, p3x, p3y):
    p3r = p3p // 10
    p3c = p3r % 10

    dice = random.randint(1, 6)

    p3p += dice

    new_p3r = p3p // 10
    new_p3c = p3p % 10

    if new_p3r > p3r:
        for x in range(48):
            move_up(p3y)
        for x in range(36 * (p3c - new_p3c)):
            move_left(p3x)
    else:
        for x in range(36 * (new_p3c - p3c)):
            move_right(p3x)

    ladder_check(p3p, p3x, p3y)
    snake_check(p3p, p3x, p3y)
    end_check(p3p)
    return p3p, p3x, p3y


def player_4_turn(p4p, p4x, p4y):
    p4r = p4p // 10
    p4c = p4r % 10

    dice = random.randint(1, 6)

    p4p += dice

    new_p4r = p4p // 10
    new_p4c = p4p % 10

    if new_p4r > p4r:
        for x in range(48):
            move_up(p4y)
        for x in range(36 * (p4c - new_p4c)):
            move_left(p4x)
    else:
        for x in range(36 * (new_p4c - p4c)):
            move_right(p4x)

    ladder_check(p4p, p4x, p4y)
    snake_check(p4p, p4x, p4y)
    end_check(p4p)
    return p4p, p4x, p4y


def ladder_check(pos, x, y):
    # L1
    if pos == 5:
        pos = 35
        for a in range(2):
            for b in range(13):
                move_right(x)
            for x in range(50):
                move_up(y)
        x = 177
        y = 171

    # L2
    if pos == 17:
        pos = 43
        for a in range(2):
            for b in range(13):
                move_left(x)
            for x in range(50):
                move_up(y)
        x = 71
        y = 214
    # L3
    if pos == 33:
        pos = 67
        for a in range(2):
            for b in range(13):
                move_left(x)
            for x in range(50):
                move_up(y)
    x = 148
    y = 210
    # L4
    if pos == 42:
        pos = 78

        for a in range(2):
            for b in range(13):
                move_right(x)
            for x in range(50):
                move_up(y)
        x = 49
        y = 239
    # L5
    if pos == 65:
        pos = 95

        for a in range(2):
            for b in range(13):
                move_left(x)
            for x in range(50):
                move_up(y)
        x = 124
        y = 300
    return pos, x, y


def snake_check(pos, x, y):
    # S1
    if pos == 32:
        pos = 8

        for a in range(2):
            for b in range(8):
                move_right(x)
            for x in range(11):
                move_down(y)

        for a in range(4):
            for b in range(13):
                move_left(x)
            for x in range(5):
                move_down(y)

        for a in range(2):
            for b in range(13):
                move_right(x)
            for x in range(11):
                move_down(y)

        for a in range(2):
            for b in range(11):
                move_left(x)

            for x in range(8):
                move_down(y)
    x = 173
    y = 30

    # S2
    if pos == 41:
        pos = 18

        for a in range(36):
            for b in range(1):
                move_right(x)
            for x in range(1):
                move_down(y)

    for a in range(2):
        for b in range(11):
            move_left(x)
        for x in range(12):
            move_down(y)

    for a in range(5):
        for b in range(6):
            move_left(x)
        for x in range(5):
            move_down(y)

    for a in range(2):
        for b in range(11):
            move_left(x)
        for x in range(20):
            move_down(y)

    x = 50
    y = 60

    # S3
    if pos == 32:
        pos = 8
    for a in range(5):
        for b in range(6):
            move_right(x)
        for x in range(7):
            move_down(y)

    for a in range(27):
        for b in range(1):
            move_left(x)
        for x in range(2):
            move_down(y)

    for a in range(2):
        for b in range(29):
            move_right(x)
        for x in range(16):
            move_down(y)

    for a in range(2):
        for b in range(13):
            move_left(x)
        for x in range(16):
            move_down(y)

    x = 99
    y = 119

    # S4
    if pos == 87:
        pos = 69

        x = 99
        y = 179

    # S5
    if pos == 99:
        pos = 56

        x = 198
        y = 140

    return pos, x, y


def end_check(pos):
    if pos == 100:
        running = False
        pygame.quit()
        sys.exit()


pygame.init()

screen = pygame.display.set_mode((300, 350))
background = pygame.image.load('background_main.png')
running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_1_points, player_1_x, player_1_y = player_1_turn(player_1_points, player_1_x, player_1_y)
            if event.key == pygame.K_d:
                player_2_points, player_2_x, player_2_y = player_2_turn(player_2_points, player_2_x, player_2_y)
            if event.key == pygame.K_w:
                player_3_points, player_3_x, player_3_y = player_3_turn(player_3_points, player_3_x, player_3_y)
            if event.key == pygame.K_s:
                player_4_points, player_4_x, player_4_y = player_4_turn(player_4_points, player_4_x, player_4_y)

    pygame.display.update()
