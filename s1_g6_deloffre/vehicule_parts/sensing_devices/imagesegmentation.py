__author__ = ["adrien_deloffre"]

""" the Imagesegmentation class calculate the coordinates of each collision box around the car (6 collision box)
    and change the appropriate boolean if the collision box collide an obstacle
"""

import pygame
from math import cos, sin, radians
from pygame.math import Vector2

class ImageSegmentation():

    def __init__(self):

        self.position_front_radar = Vector2()
        self.position_front_radar_low = Vector2()
        self.position_front_right_radar = Vector2()
        self.position_front_left_radar = Vector2()
        self.position_right_radar = Vector2()
        self.position_left_radar = Vector2()
        self.position_rear_radar = Vector2()

        self.front_collision = False
        self.rear_collision = False
        self.pedestrian_crossing = False
        self.crossroad = False
        self.touch_right = False
        self.touch_left = False
        self.turn_right = False
        self.turn_left = False

        self.ppu = 32

    def front_radar(self, car):
        self.position_front_radar.x = (car.position.x + 6.8 * cos(radians(round(car.angle)))) * self.ppu
        self.position_front_radar.y = (car.position.y - 6.8 * sin(radians(round(car.angle)))) * self.ppu

    def front_radar_low(self, car):
        self.position_front_radar_low.x = (car.position.x + 2.5 * cos(radians(round(car.angle)))) * self.ppu
        self.position_front_radar_low.y = (car.position.y - 2.5 * sin(radians(round(car.angle)))) * self.ppu

    def front_right_radar(self, car):
        self.position_front_right_radar.x = (car.position.x + 5.5 * cos(radians(round(car.angle - 23)))) * self.ppu
        self.position_front_right_radar.y = (car.position.y - 5.5 * sin(radians(round(car.angle - 23)))) * self.ppu

    def front_left_radar(self, car):
        self.position_front_left_radar.x = (car.position.x + 5.5 * cos(radians(round(car.angle + 23)))) * self.ppu
        self.position_front_left_radar.y = (car.position.y - 5.5 * sin(radians(round(car.angle + 23)))) * self.ppu

    def right_radar(self, car):
        self.position_right_radar.x = (car.position.x + 5 * cos(radians(round(car.angle - 55)))) * self.ppu
        self.position_right_radar.y = (car.position.y - 5 * sin(radians(round(car.angle - 55)))) * self.ppu

    def left_radar(self, car):
        self.position_left_radar.x = (car.position.x + 5 * cos(radians(round(car.angle + 55)))) * self.ppu
        self.position_left_radar.y = (car.position.y - 5 * sin(radians(round(car.angle + 55)))) * self.ppu

    def rear_radar(self, car):
        self.position_rear_radar.x = (car.position.x - 4.5 * cos(radians(round(car.angle)))) * self.ppu
        self.position_rear_radar.y = (car.position.y + 4.5 * sin(radians(round(car.angle)))) * self.ppu


    def update(self, car, elementlist):

        self.front_radar(car)
        self.front_radar_low(car)
        self.front_right_radar(car)
        self.front_left_radar(car)
        self.right_radar(car)
        self.left_radar(car)
        self.rear_radar(car)

        rect_front_vehicule = pygame.Rect(self.position_front_radar.x, self.position_front_radar.y, 5, 5)
        rect_front_vehicule_low = pygame.Rect(self.position_front_radar_low.x, self.position_front_radar_low.y, 5, 5)
        rect_front_right_vehicule = pygame.Rect(self.position_front_right_radar.x, self.position_front_right_radar.y, 5, 5)
        rect_front_left_vehicule = pygame.Rect(self.position_front_left_radar.x, self.position_front_left_radar.y, 5, 5)
        rect_right_vehicule = pygame.Rect(self.position_right_radar.x, self.position_right_radar.y, 5, 5)
        rect_left_vehicule = pygame.Rect(self.position_left_radar.x, self.position_left_radar.y, 5, 5)
        rect_rear_vehicule = pygame.Rect(self.position_rear_radar.x, self.position_rear_radar.y, 5, 5)

        # change the appropriate boolean according to the collision box which collides
        if rect_front_vehicule.collidelist(elementlist[0]) != -1:
            self.front_collision = True
        else:
            self.front_collision = False

        if rect_front_vehicule_low.collidelist(elementlist[1]) != -1:
            self.pedestrian_crossing = True
        else:
            self.pedestrian_crossing = False

        if rect_front_vehicule_low.collidelist(elementlist[2]) != -1:
            self.crossroad = True
        else:
            self.crossroad = False
        
        if rect_front_right_vehicule.collidelist(elementlist[0]) != -1:
            self.turn_left = True
        else:
            self.turn_left = False

        if rect_front_left_vehicule.collidelist(elementlist[0]) != -1:
            self.turn_right = True
        else:
            self.turn_right = False

        if rect_right_vehicule.collidelist(elementlist[0]) != -1:
            self.touch_right = True
        else:
            self.touch_right = False

        if rect_left_vehicule.collidelist(elementlist[0]) != -1:
            self.touch_left = True
        else:
            self.touch_left = False

        if rect_rear_vehicule.collidelist(elementlist[0]) != -1:
            self.rear_collision = True
        else:
            self.rear_collision = False