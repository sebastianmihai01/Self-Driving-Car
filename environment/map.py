import pickle
import sys
import matplotlib.pyplot as plt
import pygame
import path
from pygame import *
from PIL import Image
import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
from car import Car
from ai_brain.dqn import Dqn
import API.ray_tracing as rt

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
mouse_position = (10, 0)
drawing = False
screen = pygame.display.set_mode([WIDTH, HEIGHT])
car_png = pygame.image.load('../photos/car_updated.png')
last_x = 0
last_y = 0
n_points = 0  # the total number of points in the last drawing
length = 0  # the length of the last drawing
brain = Dqn(5, 3, 0.9)
action2rotation = [0, 20, -20]
last_reward = 0  # initializing the last reward
scores = []  # initializing the mean score curve (sliding window of the rewards) with respect to time
first_update = True  # using this trick to initialize the map only once
longueur, largeur = 1200, 750


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


def move(action, pos_x, pos_y):
    if action == 'left':
        pos_x -= 2
    elif action == 'right':
        pos_x += 2
    elif action == 'up':
        pos_y -= 2
    elif action == 'down':
        pos_y += 2
    return [pos_x, pos_y]


def setup():
    pygame.init()
    pygame.display.set_caption('Self Driving Car')
    screen.fill(BLACK)
    orientation = 0
    clock = pygame.time.Clock()
    crashed = False
    global sand  # sand is an array that has as many cells as our graphic interface has pixels. Each cell has a one if there is sand, 0 otherwise.
    global goal_x  # x-coordinate of the goal (where the car has to go, that is the airport or the downtown)
    global goal_y  # y-coordinate of the goal (where the car has to go, that is the airport or the downtown)
    sand = np.zeros((longueur, largeur))  # initializing the sand array with only zeros

    pos_x = 566
    pos_y = 66
    position = (pos_x, pos_y)
    x = 10
    y = 10
    left, right, up, down = False, False, False, False

    # draw_map()
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
        sensor1_y = pos_y - 5
        sensor2_x = pos_x + car_size_x
        sensor2_y = pos_y - 5
        sensor3_x = pos_x
        sensor3_y = car_size_y + pos_y + 5
        sensor4_x = pos_x + car_size_x
        sensor4_y = pos_y + car_size_y + 5
        sensor5_x = pos_x + car_size_x / 2
        sensor5_y = pos_y + car_size_y + 5
        sensor6_x = pos_x + car_size_x / 2
        sensor6_y = pos_y - 5

        pygame.draw.circle(screen, (254, 255, 255), (sensor1_x, sensor1_y), 5, 0)
        pygame.draw.circle(screen, green, (sensor2_x, sensor2_y), 5, 0)
        pygame.draw.circle(screen, blue, (sensor3_x, sensor3_y), 5, 0)
        pygame.draw.circle(screen, red, (sensor4_x, sensor4_y), 5, 0)
        pygame.draw.circle(screen, purple, (sensor5_x, sensor5_y), 5, 0)
        pygame.draw.circle(screen, cyan, (sensor6_x, sensor6_y), 5, 0)
        rt.calculate_distance(screen, sensor1_x, sensor2_x, sensor3_x, sensor4_x, sensor5_x, sensor6_x, sensor1_y,
                              sensor2_y, sensor3_y, sensor4_y, sensor5_y, sensor6_y)
        pygame.display.update()

        if pos_x >= WIDTH - car_size_x or \
                pos_y >= HEIGHT - car_size_y or \
                pos_x < 1 or pos_y < 1 or \
                pygame.Surface.get_at(screen, (int(pos_x - 20), int(pos_y + 20))) == (255, 255, 255) or \
                pygame.Surface.get_at(screen, (int(pos_x), int(pos_y - 20))) == (255, 255, 255) or \
                pygame.Surface.get_at(screen, (int(pos_x + 20), int(pos_y + 20))) == (255, 255, 255) or \
                pygame.Surface.get_at(screen, (int(pos_x + 20), int(pos_y - 20))) == (255, 255, 255):
            pos_x = 566
            pos_y = 66  # crashed

        position = (pos_x, pos_y)
        n = randint(1, 4)
        # left right up down
        movement = []
        if n == 1:
            movement = move('up', pos_x, pos_y)
        if n == 2:
            movement = move('left', pos_x, pos_y)
        if n == 3:
            movement = move('up', pos_x, pos_y)
        if n == 4:
            movement = move('down', pos_x, pos_y)

        pos_x = movement[0]
        pos_y = movement[1]
        screen.fill(BLACK)
        img_png = pygame.image.load("map.png")
        screen.blit(img_png, (0, 0))
        screen.blit(car_png, position)
        clock.tick(120)

        ''' TRAINING '''
        signal_car_1 = (rt.calculate_distance(screen, sensor1_x, sensor2_x, sensor3_x, sensor4_x,
                                            sensor5_x, sensor6_x, sensor1_y, sensor2_y, sensor3_y, sensor4_y,
                                            sensor5_y, sensor6_y))[0]
        signal_car_2 = (rt.calculate_distance(screen, sensor1_x, sensor2_x, sensor3_x, sensor4_x,
                                            sensor5_x, sensor6_x, sensor1_y, sensor2_y, sensor3_y, sensor4_y,
                                            sensor5_y, sensor6_y))[1]
        signal_car_3 = (rt.calculate_distance(screen, sensor1_x, sensor2_x, sensor3_x, sensor4_x,
                                            sensor5_x, sensor6_x, sensor1_y, sensor2_y, sensor3_y, sensor4_y,
                                            sensor5_y, sensor6_y))[2]
        signal_car_4 = (rt.calculate_distance(screen, sensor1_x, sensor2_x, sensor3_x, sensor4_x,
                                            sensor5_x, sensor6_x, sensor1_y, sensor2_y, sensor3_y, sensor4_y,
                                            sensor5_y, sensor6_y))[3]
        signal_car_5 = (rt.calculate_distance(screen, sensor1_x, sensor2_x, sensor3_x, sensor4_x,
                                            sensor5_x, sensor6_x, sensor1_y, sensor2_y, sensor3_y, sensor4_y,
                                            sensor5_y, sensor6_y))[4]
        signal_car_6 = (rt.calculate_distance(screen, sensor1_x, sensor2_x, sensor3_x, sensor4_x,
                                            sensor5_x, sensor6_x, sensor1_y, sensor2_y, sensor3_y, sensor4_y,
                                            sensor5_y, sensor6_y))[5]

        ''' TRAINING '''

        # current_location = [pos_x, pos_y]
        # last_location = [pos_x, pos_y]
        # orientation = [(current_location[0] - last_location[0])%360,
        #                (current_location[1] - last_location[1]) % 360]
        #
        # # last_signal = [signal_car_1, signal_car_2, signal_car_3, orientation, -orientation]
        # last_signal = []
        # action = brain.update(last_reward,
        #                       last_signal)  # playing the action from our ai (the object brain of the dqn class)
        # scores.append(brain.score())  # appending the score (mean of the last 100 rewards to the reward window)
        # rotation = action2rotation[
        #     action]  # converting the action played (0, 1 or 2) into the rotation angle (0°, 20° or -20°)
        #
        # last_location = []
        # current_location =[]



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
