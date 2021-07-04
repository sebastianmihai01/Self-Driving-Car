"""run.py: Core application of the project"""

__author__ = "Sebastian Mihai"
__copyright__ = "Copyright 2021, The comfort of my bedroom"

import math as maths
import sys

import numpy as np
import pygame
from pygame import *

import API.ray_tracing as rt
from ai_brain.dqn import Dqn

WHITE, BLACK, cyan, purple = (255, 255, 255), (0, 0, 0), (0, 255, 255), (238, 130, 238)
red, green, blue = (255, 0, 0), (0, 255, 0), (0, 0, 255)
WIDTH, HEIGHT = 1200, 750
car_size_x, car_size_y = 60, 30
screen = pygame.display.set_mode([WIDTH, HEIGHT])
car_png = pygame.image.load('../photos/car_updated.png')
brain = Dqn(5, 3, 0.9)
reward_prev, angle, new_angle, last_distance = 0, 0, 0, 0
scores, obstacle = [], []
last_rotation = None
goal = 1
goal_coord_x, goal_coord_y = 0, 0
action = ''

'''
    Function to calculate the distance to the next set goal
    > Used to determine the current reward for the agent
'''


def calculate_distance(coord_x, coord_y, goal_number):
    local_x, local_y = 0, 0
    dist = 0

    # goal up (1): 566, 66
    # goal right (2) : 1040, 390
    # goal down (3): 600, 646
    # goal left (4): 102, 384

    if goal_number == 1:
        dist = maths.sqrt(pow(566 - coord_x, 2) + pow(66 - coord_y, 2))

    elif goal_number == 2:
        dist = maths.sqrt(pow(1040 - coord_x, 2) + pow(390 - coord_y, 2))

    elif goal_number == 3:
        dist = maths.sqrt(pow(600 - coord_x, 2) + pow(646 - coord_y, 2))

    elif goal_number == 4:
        dist = maths.sqrt(pow(102 - coord_x, 2) + pow(384 - coord_y, 2))

    return dist


'''
    Function to set the next goal, if the current goal has been reached
    > Goals are incrementally updated, clockwise from the start position of the car, in the middle of the road
'''


def set_goal(coord_x, coord_y, goal_number):
    global goal
    finished = False

    if goal_number == 2:
        if 1000 < coord_x < 1080 and 360 < coord_y < 420:
            finished = True
            goal = 3

    if goal_number == 3:
        if 520 < coord_x < 570 and 30 < coord_y < 700:
            finished = True
            goal = 4

    if goal_number == 4:
        if 520 < coord_x < 170 and 30 < coord_y < 410:
            finished = True
            goal = 1

    if goal_number == 1:
        if 520 < coord_x < 590 and 30 < coord_y < 90:
            finished = True
            goal = 2

    return finished


'''
    Function to create custom maps
'''


def draw_map():
    global screen
    finished = False
    size = (3, 3)
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


'''
    Function which will help in the action selection policy later on
'''


def move(picked_action, pos_x, pos_y):
    if picked_action == 'left':
        pos_x -= 2
    elif picked_action == 'right':
        pos_x += 2
    elif picked_action == 'up':
        pos_y -= 2
    elif picked_action == 'down':
        pos_y += 2

    return [pos_x, pos_y]


'''
    Function to rotate the image within it's own (gravitational) center
    
'''


def rotate(png, centrum, rotation_degree):
    # Rotate the image for "rotation_degree" radians
    updated_png = pygame.transform.rotate(png, rotation_degree)
    # Set the new centre so that the image will not drift away as it shifts axis while rotated
    centrum = updated_png.get_rect(center=centrum.center)
    # Return the modified variables

    return updated_png, centrum


def run():
    pygame.init()
    pygame.display.set_caption('Self Driving Car')
    screen.fill(BLACK)
    radians = 0
    frames = pygame.time.Clock()
    crashed = False
    global obstacle, last_rotation

    # fill the numpy array with 0
    # this will represent the array of pixels, of which some will be 0 and others 1
    # depending on the obstacle drawing
    obstacle = np.zeros((WIDTH, HEIGHT))
    for i in range(0, 1200):
        for j in range(0, 750):
            # if pixel is 1 (obstacle)
            if pygame.Surface.get_at(screen, (i, j)) == (255, 255, 255):
                obstacle[i][j] = 1

    last_rotation = 'down'
    global angle, new_angle, action, car_png
    global last_distance
    global reward_prev

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

        centrum = car_png.get_rect(center=(pos_x + 30, pos_y + 15))
        last_image = car_png
        orig_image = car_png
        image, centrum = rotate(orig_image, centrum, angle)
        last_rotation = ''

        if action == 'left':
            pos_x -= 3
            if last_rotation != 'left' and new_angle != 180:
                angle = 180
                new_angle = 180
                last_rotation = 'left'

        if action == 'right':
            pos_x += 3
            if last_rotation != 'right' and new_angle != 90:
                angle = 0
                new_angle = 90
                last_rotation = 'right'

        if action == 'up':
            pos_y -= 3
            if last_rotation != 'up' and new_angle != 90:
                angle = 90
                new_angle = 90
                last_rotation = 'up'

        if action == 'down':
            pos_y += 3
            if last_rotation != 'down' and new_angle != 270:
                angle = 270
                new_angle = 270
                last_rotation = 'down'

        """ Sensors' coordinates and setup  """

        sensor1_x, sensor1_y = pos_x, pos_y - 5
        sensor2_x, sensor2_y = pos_x + car_size_x, pos_y - 5
        sensor3_x, sensor3_y = pos_x, car_size_y + pos_y + 5
        sensor4_x, sensor4_y = pos_x + car_size_x, pos_y + car_size_y + 5
        sensor5_x, sensor5_y = pos_x + car_size_x / 2, pos_y + car_size_y + 5
        sensor6_x, sensor6_y = pos_x + car_size_x / 2, pos_y - 5

        pygame.draw.circle(screen, (254, 255, 255), (sensor1_x, sensor1_y), 5, 0)
        pygame.draw.circle(screen, green, (sensor2_x, sensor2_y), 5, 0)
        pygame.draw.circle(screen, blue, (sensor3_x, sensor3_y), 5, 0)
        pygame.draw.circle(screen, red, (sensor4_x, sensor4_y), 5, 0)
        pygame.draw.circle(screen, purple, (sensor5_x, sensor5_y), 5, 0)
        pygame.draw.circle(screen, cyan, (sensor6_x, sensor6_y), 5, 0)
        rt.calculate_distance(screen, sensor1_x, sensor2_x, sensor3_x, sensor4_x, sensor5_x, sensor6_x, sensor1_y,
                              sensor2_y, sensor3_y, sensor4_y, sensor5_y, sensor6_y)
        pygame.display.update()

        new_crushed = False
        if pos_x >= WIDTH - car_size_x or \
                pos_y >= HEIGHT - car_size_y or \
                pos_x < 1 or pos_y < 1 or \
                pygame.Surface.get_at(screen, (int(pos_x - 20), int(pos_y + 20))) == (255, 255, 255) or \
                pygame.Surface.get_at(screen, (int(pos_x), int(pos_y - 20))) == (255, 255, 255) or \
                pygame.Surface.get_at(screen, (int(pos_x + 20), int(pos_y + 20))) == (255, 255, 255) or \
                pygame.Surface.get_at(screen, (int(pos_x + 20), int(pos_y - 20))) == (255, 255, 255):
            pos_x = 566
            pos_y = 66  # crashed
            new_crushed = True

        position = (pos_x, pos_y)
        screen.fill(BLACK)
        img_png = pygame.image.load("map.png")
        screen.blit(img_png, (0, 0))
        screen.blit(image, centrum)
        pygame.display.flip()
        frames.tick(120)

        ''' TRAINING 1 '''
        signal_list = (rt.calculate_distance(screen, sensor1_x, sensor2_x, sensor3_x, sensor4_x,
                                             sensor5_x, sensor6_x, sensor1_y, sensor2_y, sensor3_y, sensor4_y,
                                             sensor5_y, sensor6_y))

        signal_car_1, signal_car_2, signal_car_3, signal_car_4, signal_car_5, signal_car_6 \
            = signal_list[0], signal_list[1], signal_list[2], signal_list[3], signal_list[4], signal_list[5]

        ''' TRAINING 2 '''
        sensor_signal_one, sensor_signal_two, sensor_signal_three = 0, 0, 0

        # updating the signals
        #
        # we take all the cells from -dim to +dim => we form a dim x dim square => density cell in obstacle
        # obstacles are either 0 or 1

        dim = 35
        first = obstacle[sensor1_x - dim:sensor1_x + 20, sensor1_y - dim:sensor1_y + 20]
        second = obstacle[sensor2_x - dim:sensor2_x + 20, sensor2_y - dim:sensor2_y + 20]
        third = obstacle[sensor3_x - dim:sensor3_x + 20, sensor3_y - dim:sensor3_y + 20]

        sensor_signal_one, sensor_signal_two, sensor_signal_three = np.sum(first) / maths.pow(dim, 2), \
                                                                    np.sum(second) / maths.pow(dim, 2), np.sum(
            third) / maths.pow(dim, 2)

        """ REWARD """
        distance = calculate_distance(pos_x, pos_y, goal)

        if distance - last_distance < 0:
            reward_prev = 0.01
        else:
            reward_prev = -0.1

        """ REACHED GOAL """
        if set_goal(pos_x, pos_y, goal) is True:
            reward_prev = 1

        last_distance = distance

        """ DECISION SELECTION PROCESS"""
        if sensor_signal_one > 0 or sensor_signal_two > 0 or sensor_signal_three > 0:
            reward_prev = -0.5

        if new_crushed is True:
            reward_prev = -1
        signal_prev = [sensor_signal_one, sensor_signal_two, sensor_signal_three, radians, -radians]
        action = brain.update(reward_prev,
                              signal_prev)
        scores.append(brain.score())
        print(reward_prev)

    pygame.quit()


run()
