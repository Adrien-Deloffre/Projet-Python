__author__ = ["adrien_deloffre"]

""" the Ranger class calculate the distance between the front of the car and the nearest obstacle in front """

import pygame
from math import sqrt, cos, sin, tan, radians
from pygame.math import Vector2

class Ranger():

    def __init__(self):

        self.position_front_lidar = Vector2()

        self.front_distance = 0
        self.rear_distance = 0
        self.right_distance = 0
        self.left_distance = 0

        self.bool_front_lidar = False

        self.ppu = 32

    # calculate the distance between two coordinates (x1,y1) and (x2,y2)
    def distance(self, x1, y1, x2, y2):
        d = sqrt((x2-x1)**2 + (y2-y1)**2)
        return d
        

    def update(self, car, elementlist):

        i = 0
        # while the rectangle of the lidar doesn't collide, it advances
        while self.bool_front_lidar == False:
            i+=0.1
            self.position_front_lidar.x = (car.position.x + i * cos(radians(round(car.angle)))) * self.ppu
            self.position_front_lidar.y = (car.position.y - i * sin(radians(round(car.angle)))) * self.ppu
            rect_front_lidar = pygame.Rect(self.position_front_lidar.x, self.position_front_lidar.y, 2, 2)
            if rect_front_lidar.collidelist(elementlist[0]) != -1:
                self.bool_front_lidar = True
            else:
                self.bool_front_lidar = False

        self.front_distance = self.distance(car.position.x, car.position.y, self.position_front_lidar.x/self.ppu, self.position_front_lidar.y/self.ppu) - 2
        self.bool_front_lidar = False