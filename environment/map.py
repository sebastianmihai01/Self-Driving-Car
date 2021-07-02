import sys
import matplotlib.pyplot as plt
import pygame
from pygame import *
from PIL import Image
import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
from car import Car


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
cyan = (0, 255, 255)
purple = (238, 130, 238)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
WIDTH = 1200
HEIGHT = 750
car_size_x = 60  # to help us determine crashes better
car_size_y = 30
mouse_position = (0, 0)
drawing = False
screen = pygame.display.set_mode([WIDTH, HEIGHT])
car_png = pygame.image.load('../photos/car_updated.png')

def draw_map():
    global screen
    finished = False
    size = (3, 3)
    radius = 25
    circle = pygame.Surface(size)
    last_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEMOTION:
                if (finished):
                    mouse_position = pygame.mouse.get_pos()
                    if last_pos is not None:
                        pygame.draw.line(screen, WHITE, last_pos, mouse_position, 4)
                    last_pos = mouse_position
            elif event.type == MOUSEBUTTONUP:
                mouse_position = (0, 0)
                last_pos = None
                finished = False
            elif event.type == MOUSEBUTTONDOWN:
                finished = True
        pygame.display.update()

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

    #draw_map()
    running = True
    while running is True and crashed is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

        sensor1_x = pos_x
        sensor1_y = pos_y-5
        sensor2_x = pos_x+car_size_x
        sensor2_y = pos_y-5
        sensor3_x = pos_x
        sensor3_y = car_size_y+pos_y + 5
        sensor4_x = pos_x+car_size_x
        sensor4_y = pos_y+car_size_y+5
        sensor5_x = pos_x+car_size_x/2
        sensor5_y = pos_y+car_size_y+5
        sensor6_x = pos_x+car_size_x/2
        sensor6_y = pos_y-5

        pygame.draw.circle(screen, WHITE, (sensor1_x, sensor1_y), 5, 0)
        pygame.draw.circle(screen, green, (sensor2_x, sensor2_y), 5, 0)
        pygame.draw.circle(screen, blue, (sensor3_x, sensor3_y), 5, 0)
        pygame.draw.circle(screen, red, (sensor4_x, sensor4_y), 5, 0)
        pygame.draw.circle(screen, purple, (sensor5_x, sensor5_y), 5, 0)
        pygame.draw.circle(screen, cyan, (sensor6_x, sensor6_y), 5, 0)
        pygame.display.update()

        if pos_x >= WIDTH - car_size_x or \
                pos_y >= HEIGHT - car_size_y or \
                pos_x < 1 or pos_y < 1:
            pos_x = pos_y = 1  # crashed

        position = (pos_x, pos_y)
        pygame.draw.rect(screen, WHITE, (200, 150, 100, 50))
        screen.fill(BLACK)
        screen.blit(car_png, position)
        clock.tick(120)

    pygame.quit()

    def save(self, obj):  # save button
        score = 0
        print("saving brain...")
        # agent.save()
        plt.plot(score)
        plt.show()

    def load(self, obj):  # load button
        print("loading last saved brain...")
        # agent.load()


setup()