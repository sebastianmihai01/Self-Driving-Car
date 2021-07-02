import numpy as np
import sys
import matplotlib.pyplot as plt
import pygame
from pygame import *
from PIL import Image
import numpy as np
from random import random, randint
import matplotlib.pyplot as plt

global x, y, sensor1, sensor2, sensor3, screen, car_size_x, car_size_y
car_png = pygame.image.load('../photos/car_updated.png')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
cyan = (0, 255, 255)
purple = (238, 130, 238)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Car:
    def __init__(self, screen, x, y, car_size_x, car_size_y):
        screen.blit(car_png, (x, y))
        image_car = Image.open('../photos/car.png')
        new_image = image_car.resize((car_size_x, car_size_y))
        new_image.save('car_updated.png')

#
#
# from random import random, randint
# import matplotlib.pyplot as plt
#
# class Car(Widget):
#     # angle = angle between OX and the car
#     angle = NumericProperty(0)
#     # last rotation of the car (after the action, => rotation of 0, 20 or -20 degrees)
#     rotation = NumericProperty(0)  # initializing the
#
#     # velocity vector
#     velocity_x = NumericProperty(0)  # coord X of the velocity vector
#     velocity_y = NumericProperty(0)  # coord Y of the velocity vector
#     velocity = list(velocity_x, velocity_y)
#
#     # ---------------------------------------
#
#     # Sensors
#     # First one(1) = looks forward
#     # Second one(2) = looks 30 degrees to the left
#     # Third one(3) - looks 30 degrees to the right
#
#     # Each sensor has X and Y coordinates
#     # Each sensor is composed by a Sensor Vector
#
#     sensor1_x = NumericProperty(0)
#     sensor1_y = NumericProperty(0)
#     sensor1 = list(sensor1_x, sensor1_y)
#
#     sensor2_x = NumericProperty(0)
#     sensor2_y = NumericProperty(0)
#     sensor2 = list(sensor2_x, sensor2_y)
#
#     sensor3_x = NumericProperty(0)
#     sensor3_y = NumericProperty(0)
#     sensor3 = list(sensor3_x, sensor3_y)
#
#     # ---------------------------------------
#     # Signals
#     # Signal 1 = Signal received from Sensor 1
#
#     # Signal = Density
#
#     # Density
#     # 1. Take big squares around the sensors (200x200)
#     # 2. Divide the number of '1' by the number of cells
#     # 3. As '1' corresponds to the sand => we find the density
#     # 4. We do this for each sensor
#
#     signal1 = NumericProperty(0)  # initializing the signal received by sensor 1
#     signal2 = NumericProperty(0)  # initializing the signal received by sensor 2
#     signal3 = NumericProperty(0)  # initializing the signal received by sensor 3
#
#     # ---------------------------------------
#
#     def move(self, rotation, sand):
#
#         # the direction will be updated in the direction of the velocity vector
#         # the second self.pos = last position of the car
#         self.pos = Vector(*self.velocity) + self.pos
#
#         # update the rotation of the car by [0,20,-20]
#         self.rotation = rotation
#
#         # update the angle by -> angle between the OX and the AXIS of DIRECTION of the car
#         self.angle = self.angle + self.rotation
#
#         # after the car has moved => update sensors & signals
#         # ---
#         # if the car rotates => the sensors rotate as well => we need to update them
#         # ---
#         # the '30' from vector(30, 0) is the DISTANCE between the CAR and the SENSOR
#         # or: distance between the car and what the car detects
#         self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos  # updating the position of sensor 1
#         self.sensor2 = Vector(30, 0).rotate((self.angle + 30) % 360) + self.pos  # updating the position of sensor 2
#         self.sensor3 = Vector(30, 0).rotate((self.angle - 30) % 360) + self.pos  # updating the position of sensor 3
#
#         # updating the signals
#         #
#         # 1. we take all the cells from -10 to +10 => we form a 20x20 square => 400 cells
#         # 2. in this square, we sum up the cells (because they are either 0 or 1)
#         # 3. we divide by 400 to find the DENSITY of obstacles
#         self.signal1 = int(np.sum(sand[int(self.sensor1_x) - 10:int(self.sensor1_x) + 10, int(self.sensor1_y) - 10:int(
#             self.sensor1_y) + 10])) / 400.  # getting the signal received by sensor 1 (density of sand around sensor 1)
#         self.signal2 = int(np.sum(sand[int(self.sensor2_x) - 10:int(self.sensor2_x) + 10, int(self.sensor2_y) - 10:int(
#             self.sensor2_y) + 10])) / 400.  # getting the signal received by sensor 2 (density of sand around sensor 2)
#         self.signal3 = int(np.sum(sand[int(self.sensor3_x) - 10:int(self.sensor3_x) + 10, int(self.sensor3_y) - 10:int(
#             self.sensor3_y) + 10])) / 400.  # getting the signal received by sensor 3 (density of sand around sensor 3)
#
#         # punishment
#         #
#         # we punish the car when it goes too close to a wall
#         # longueur-10 = 10 cells from the bottom right corner (on the OX)
#         # ----------------  => straight line going up on the OY axis (parallel to the right side of the map, and at a distance of 10)
#         #
#         # or's = right,left,upper,bottom edges of the map
#         #
#         # signal = 1 => density full of sand => car will get a terrible reward
#
#         if self.sensor1_x > longueur - 10 or self.sensor1_x < 10 or self.sensor1_y > largeur - 10 or self.sensor1_y < 10:  # if sensor 1 is out of the map (the car is facing one edge of the map)
#             self.signal1 = 1.  # sensor 1 detects full sand
#         if self.sensor2_x > longueur - 10 or self.sensor2_x < 10 or self.sensor2_y > largeur - 10 or self.sensor2_y < 10:  # if sensor 2 is out of the map (the car is facing one edge of the map)
#             self.signal2 = 1.  # sensor 2 detects full sand
#         if self.sensor3_x > longueur - 10 or self.sensor3_x < 10 or self.sensor3_y > largeur - 10 or self.sensor3_y < 10:  # if sensor 3 is out of the map (the car is facing one edge of the map)
#             self.signal3 = 1.  # sensor 3 detects full sand
#
#
# class Ball1(Widget):
#     pass
#
#
# class Ball2(Widget):
#     pass
#
#
# class Ball3(Widget):
#     pass
#
#
#
#
# class Game(Widget):
#     car = Sensor(None)  # getting the car object from our kivy file
#     ball1 = Sensor(None)  # getting the sensor 1 object from our kivy file
#     ball2 = Sensor(None)  # getting the sensor 2 object from our kivy file
#     ball3 = Sensor(None)  # getting the sensor 3 object from our kivy file
#
#     def serve_car(self):  # starting the car when we launch the application
#         self.car.center = self.center  # the car will start at the center of the map
#         self.car.velocity = Vector(6, 0)  # the car will start to go horizontally to the right with a speed of 6
#
#     def update(self,
#                dt, sand):  # the big update function that updates everything that needs to be updated at each discrete time t when reaching a new state (getting new signals from the sensors)
#
#         global brain  # specifying the global variables (the brain of the car, that is our AI)
#         global last_reward  # specifying the global variables (the last reward)
#         global scores  # specifying the global variables (the means of the rewards)
#         global last_distance  # specifying the global variables (the last distance from the car to the goal)
#         global goal_x  # specifying the global variables (x-coordinate of the goal)
#         global goal_y  # specifying the global variables (y-coordinate of the goal)
#         global longueur  # specifying the global variables (width of the map)
#         global largeur  # specifying the global variables (height of the map)
#         first_update = False
#
#         longueur = self.width  # width of the map (horizontal edge)
#         largeur = self.height  # height of the map (vertical edge)
#         if first_update:  # trick to initialize the map only once
#             self.init()
#
#         xx = goal_x - self.car.x  # difference of x-coordinates between the goal and the car
#         yy = goal_y - self.car.y  # difference of y-coordinates between the goal and the car
#         orientation = Vector(*self.car.velocity).angle((xx,
#                                                         yy)) / 180.  # direction of the car with respect to the goal (if the car is heading perfectly towards the goal, then orientation = 0)
#
#
#
#
#         # brain = object of the DQN class
#         # action is the output of our Neural Network
#         #
#         # it takes: last reward obtained by the car
#         #           last signal = signal1,2,3 from sensors1,2,3
#         #
#         # orientation
#         # forward = 0
#         # slightly to the right = 5 degrees
#         #
#         # last param: '-orientation' means that we force the AI to search both directions (front and back, left and right)
#         #
#         # these 5 params = inputs of our ENCODED VECTOR, which will go into the network (INPUT VECTOR)
#         # after it goes into the network => it returns the output = action to play at each time (by the 'action' variable)
#
#         last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation]
#         action = brain.update(last_reward,
#                               last_signal)  # playing the action from our ai (the object brain of the dqn class)
#         scores.append(brain.score())  # appending the score (mean of the last 100 rewards to the reward window)
#         rotation = rot.rotate(self, action)  # converting the action played (0, 1 or 2) into the rotation angle (0°, 20° or -20°)
#
#
#
#
#         #move function - used to move the car using the rotation
#         self.car.move(rotation)  # moving the car according to this last rotation angle
#         distance = np.sqrt((self.car.x - goal_x) ** 2 + (
#                 self.car.y - goal_y) ** 2)  # getting the new distance between the car and the goal right after the car moved
#         self.ball1.pos = self.car.sensor1  # updating the position of the first sensor (ball1) right after the car moved
#         self.ball2.pos = self.car.sensor2  # updating the position of the second sensor (ball2) right after the car moved
#         self.ball3.pos = self.car.sensor3  # updating the position of the third sensor (ball3) right after the car moved
#
#
#
#
#         # when the car goes into some sand
#         #
#         # 1. we reduce its velocity (initial velocity = 6 and slowed down to 1 if stepped in sand)
#         # 2. the agent gets a bad reward (-1 reward, worst possible - and the best is 1)
#         if sand[int(self.car.x), int(self.car.y)] > 0:  # if the car is on the sand
#             self.car.velocity = Vector(1, 0).rotate(self.car.angle)  # it is slowed down (speed = 1)
#             last_reward = -1  # and reward = -1
#         else:
#
#
#
#             # if not in sand
#             # 1. if it goes closer to the goal => it gets a 0.1 reward
#             # 1.1 if it gets further away from the goal => it gets a -0.2 reward
#             self.car.velocity = Vector(6, 0).rotate(self.car.angle)  # it goes to a normal speed (speed = 6)
#             last_reward = -0.2  # and it gets bad reward (-0.2)
#             if distance < last_distance:  # however if it getting close to the goal
#                 last_reward = 0.1  # it still gets slightly positive reward 0.1
#
#
#
#
#         # other
#         # 1. if car gets too close to one of the edges => not slowed down BUT bad reward (-1)
#         if self.car.x < 10: # too close to the left side
#             self.car.x = 10
#             last_reward = -1
#
#         # other
#         # 2. same but with the right side of the map
#         if self.car.x > self.width - 10:
#             self.car.x = self.width - 10  # it is not slowed down
#             last_reward = -1  # but it gets bad reward -
#
#         # bottom
#         if self.car.y < 10:
#             self.car.y = 10
#             last_reward = -1
#
#         # upper
#         if self.car.y > self.height - 10:
#             self.car.y = self.height - 10
#             last_reward = -1
#
#
#         # Car reaches the goal (either airport/downtown)
#         # 1. distance < 100: in the area of the goal
#         # 2. we update the COORDINATES of the new goal to the different location (airport->downtown and vice-versa)
#         if distance < 100:
#             goal_x = self.width - goal_x  # the goal becomes the bottom right corner of the map
#             goal_y = self.height - goal_y  # the goal becomes the bottom right corner of the map
#
#         # Updating the last distance from the car to the goal
#         last_distance = distance
