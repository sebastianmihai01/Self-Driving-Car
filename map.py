import sys
import tkinter

import pygame
from pygame import *
from PIL import Image

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 1200
HEIGHT = 750
car_size_x = 60 # to help us determine crashes better
car_size_y = 30
screen = pygame.display.set_mode([WIDTH, HEIGHT])
car_png = pygame.image.load('car_updated.png')


def car(x, y):
    screen.blit(car_png, (x, y))
    image = Image.open('car.png')
    new_image = image.resize((car_size_x, car_size_y))
    new_image.save('car_updated.png')


def setup():
    pygame.init()
    pygame.display.set_caption('Self Driving Car')
    screen.fill(BLACK)
    clock = pygame.time.Clock()
    crashed = False

    pos_x = 1
    pos_y = 1
    position = (pos_x, pos_y)
    x = 1
    y = 1
    left, right, up, down = False, False, False, False

    running = True
    while running is True and crashed is False:

        # pos_x += 2
        # pos_y += 2

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_a:  # use constants K_a
                    left = True
                elif event.key == K_d:  # use constants K_d
                    right = True
                elif event.key == K_w:  # use constants K_w
                    up = True
                elif event.key == K_s:  # use constants K_s
                    down = True

            if event.type == KEYUP:
                if event.key == K_a:  # use constants K_a
                    left = False
                elif event.key == K_d:  # use constants K_d
                    right = False
                elif event.key == K_w:  # use constants K_w
                    up = False
                elif event.key == K_s:  # use constants K_s
                    down = False

        if left:
            pos_x -= 2
        if right:
            pos_x += 2
        if up:
            pos_y -= 2
        if down:
            pos_y += 2

        if pos_x >= WIDTH - car_size_x or pos_y >= HEIGHT - car_size_y:
            crashed = True

        position = (pos_x, pos_y)
        # if user clicks on X
        car(x, y)
        pygame.draw.rect(screen, WHITE, (200, 150, 100, 50))
        screen.fill(BLACK)
        screen.blit(car_png, position)
        pygame.display.update() # updates the frames
        clock.tick(120)

    pygame.quit()


def __init__():
    setup()


__init__()
