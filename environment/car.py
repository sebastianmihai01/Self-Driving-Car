import pygame
from PIL import Image

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
