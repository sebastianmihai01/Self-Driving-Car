import pygame
# import vector as Vector
import API.rotation as r
import dqn as brain

'''

get the color value at a single pixel get_at((x, y)) -> Color

'''
import pygame
import API.vector

white = (255, 255, 255)
red = (255, 0, 0)
goal_x = 0
goal_y = 0
last_distance = 0
distance = 0
scores = []


def calculate_distance(screen, s1_x, s2_x, s3_x, s4_x, s5_x, s6_x, s1_y, s2_y, s3_y, s4_y, s5_y, s6_y):
    ray1, ray2, ray3, ray4, ray5, ray6 = 0, 0, 0, 0, 0, 0  # distances from the sensor to the closest wall
    black = (0, 0, 0)
    current_pixel = None
    distance_list = []
    dim1_x = s1_x
    dim1_y = s1_y
    dim2_x = s2_x
    dim2_y = s2_y
    dim3_x = s3_x
    dim3_y = s3_y
    dim4_x = s4_x
    dim4_y = s4_y
    dim5_x = s5_x
    dim5_y = s5_y
    dim6_x = s6_x
    dim6_y = s6_y

    # stanga-sus
    # while current_pixel != (255, 255, 255)
    if 0 < dim1_x < 1150 and 0 < dim1_y < 700:
        while 1 < dim1_x < 1149 and 1 < dim1_y < 749:
            ray1 += 1
            dim1_x -= 1
            dim1_y -= 1
            if pygame.Surface.get_at(screen, (int(dim1_x), int(dim1_y))) != white:
                pygame.Surface.set_at(screen, (int(dim1_x), int(dim1_y)), red)
            else:
                break
            distance_list.append(ray1)

    # return
    if 0 < dim2_x < 1150 and 0 < dim2_y < 700:
        while 1 < dim2_x < 1149 and 1 < dim2_y < 749:
            ray2 += 1
            dim2_x += 1
            dim2_y -= 1
            if pygame.Surface.get_at(screen, (int(dim2_x), int(dim2_y))) != white:
                pygame.Surface.set_at(screen, (dim2_x, dim2_y), red)
            else:
                break
            distance_list.append(ray2)

    # dreapta sus
    if 0 < dim3_x < 1150 and 0 < dim3_y < 700:
        while 1 < dim3_x < 1149 and 1 < dim3_y < 749 and pygame.Surface.get_at(screen, (int(dim3_x), int(dim3_y))) != (
                255, 255, 255):
            ray3 += 1
            dim3_x -= 1
            dim3_y += 1
            if pygame.Surface.get_at(screen, (int(dim3_x), int(dim3_y))) != white:
                pygame.Surface.set_at(screen, (dim3_x, dim3_y), red)
            else:
                break
            distance_list.append(ray3)

    # dreapta jos
    if 0 < dim4_x < 1150 and 0 < dim4_y < 700:
        while 1 < dim4_x < 1149 and 1 < dim4_y < 749 and pygame.Surface.get_at(screen, (int(dim4_x), int(dim4_y))) != (
                255, 255, 255):
            ray4 += 1
            dim4_x += 1
            dim4_y += 1
            if pygame.Surface.get_at(screen, (int(dim4_x), int(dim4_y))) != white:
                pygame.Surface.set_at(screen, (dim4_x, dim4_y), red)
            else:
                break
            distance_list.append(ray4)

    #  jos
    if 0 < dim5_x < 1150 and 0 < dim5_y < 700:
        while 1 < dim5_x < 1149 and 1 < dim5_y < 749 and pygame.Surface.get_at(screen, (int(dim5_x), int(dim5_y))) != (
                255, 255, 255):
            ray5 += 1
            dim5_y += 1
            if pygame.Surface.get_at(screen, (int(dim5_x), int(dim5_y))) != white:
                pygame.Surface.set_at(screen, (int(dim5_x), int(dim5_y)), red)
            else:
                break
            distance_list.append(ray5)

    # stanga jos
    if 0 < dim6_x < 1150 and 0 < dim6_y < 700:
        while 1 < dim6_x < 1149 and 1 < dim6_y < 749 and pygame.Surface.get_at(screen, (int(dim6_x), int(dim6_y))) != (
                255, 255, 255):
            ray6 += 1
            # dim6_x += 1
            dim6_y -= 1
            if pygame.Surface.get_at(screen, (int(dim6_x), int(dim6_y))) != white:
                pygame.Surface.set_at(screen, (int(dim6_x), int(dim6_y)), red)
            else:
                break
            distance_list.append(ray6)

    return [[dim1_x, dim1_y], [dim2_x, dim2_y],
            [dim3_x, dim3_y], [dim4_x, dim4_y],
            [dim5_x, dim5_y], [dim6_x, dim6_y]]


def crashed(self, x, y, s1_x, s2_x, s3_x, s4_x, s5_x, s6_x, s1_y, s2_y, s3_y, s4_y, s5_y, s6_y):
    global white
    last_distance = 0
    still_alive = False
    last_reward = 0
    global scores
    self.x = x
    self.y = y
    self.s1_x = s1_x
    self.s2_x = s2_x
    self.s3_x = s3_x
    self.s4_x = s4_x
    self.s5_x = s5_x
    self.s6_x = s6_x
    self.s1_y = s1_y
    self.s2_y = s2_y
    self.s3_y = s3_y
    self.s4_y = s4_y
    self.s5_y = s5_y
    self.s6_y = s6_y
    crash = False

    if pygame.Surface.get_at(x, y) == white or \
            pygame.Surface.get_at(s1_x, s1_y) == white or \
            pygame.Surface.get_at(s2_x, s2_y) == white or \
            pygame.Surface.get_at(s3_x, s3_y) == white or \
            pygame.Surface.get_at(s4_x, s4_y) == white or \
            pygame.Surface.get_at(s5_x, s5_y) == white or \
            pygame.Surface.get_at(s6_x, s6_y) == white:
        crash = True
        return crash
    else:
        xx = goal_x - self.x
        yy = goal_y - self.y
        # orientation = vector.Vector(*self.car.velocity).angle((xx,yy))/180.
        # last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation]

        # action = brain.update(last_reward, last_signal)
        scores.append(brain.score())
        # rotation = r.rotate(self, action)

        if pygame.Surface.get_at(x, y) != white:
            # self.car.velocity = Vector(1, 0).rotate(self.car.angle)
            last_reward = -1
        else:  # otherwise
            # self.car.velocity = Vector(6, 0).rotate(self.car.angle)
            last_reward = -0.2
            if distance < last_distance:
                last_reward = 0.1

        if self.car.x < 10:
            self.car.x = 10
            last_reward = -1
        if self.car.x > self.width - 10:
            self.car.x = self.width - 10
            last_reward = -1
        if self.car.y < 10:
            self.car.y = 10
            last_reward = -1
        if self.car.y > self.height - 10:
            self.car.y = self.height - 10
            last_reward = -1

        if distance < 100:
            last_reward = +1

        if still_alive:
            last_reward = +0.2
        last_distance = distance
