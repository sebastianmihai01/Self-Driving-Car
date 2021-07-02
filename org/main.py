import numpy as np
import matplotlib.pyplot as plt

import API.carApp
from ai_brain.dqn import Dqn

last_x = 0
last_y = 0
n_points = 0
length = 0

brain = Dqn(5,3,0.9)
action2rotation = [0,20,-20]
last_reward = 0
scores = []
first_update = True
longueur = largeur = 0

Widget = None

def init():
    global sand
    global goal_x
    global goal_y
    global first_update
    sand = np.zeros((longueur,largeur))
    goal_x = 20
    goal_y = largeur - 20
    first_update = False

last_distance = 0


class Ball1(Widget):
    pass
class Ball2(Widget):
    pass
class Ball3(Widget):
    pass
# Running the whole thing
if __name__ == '__main__':
    API.carApp.CarApp().run()
