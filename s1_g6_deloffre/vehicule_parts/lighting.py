__author__ = ["adrien_deloffre"]

""" the Lighting class calculate the coordinates of each light """

import pygame
from math import sin, cos, radians
from pygame.math import Vector2

class Lighting():

    def __init__(self):

        self.position_low_beam = Vector2()
        self.position_high_beam = Vector2()
        self.position_right_blink = Vector2()
        self.position_left_blink = Vector2()
        self.position_rear_beam = Vector2()

        self.low_beam_distance = 2.6
        self.high_beam_distance = 3.4
        self.blink_distance = 1
        self.rear_beam_distance = self.low_beam_distance

        self.low_beam_image = pygame.image.load("img/low_beam.png").convert_alpha()
        self.high_beam_image = pygame.image.load("img/high_beam.png").convert_alpha()
        self.right_blink_image = pygame.image.load("img/right_blink.png").convert_alpha()
        self.left_blink_image = pygame.image.load("img/left_blink.png").convert_alpha()
        self.rear_beam_image = pygame.image.load("img/rear_beam.png").convert_alpha()


    def low_beam(self, car):
        self.position_low_beam.x = car.position.x + self.low_beam_distance * cos(radians(round(car.angle)))
        self.position_low_beam.y = car.position.y - self.low_beam_distance * sin(radians(round(car.angle)))


    def high_beam(self, car):
        self.position_high_beam.x = car.position.x + self.high_beam_distance * cos(radians(round(car.angle)))
        self.position_high_beam.y = car.position.y - self.high_beam_distance * sin(radians(round(car.angle)))


    def blink_right(self, car):
        self.position_right_blink.x = car.position.x - self.blink_distance * sin(radians(round(-1*car.angle)))
        self.position_right_blink.y = car.position.y + self.blink_distance * cos(radians(round(car.angle)))


    def blink_left(self, car):
        self.position_left_blink.x = car.position.x - self.blink_distance * sin(radians(round(car.angle)))
        self.position_left_blink.y = car.position.y - self.blink_distance * cos(radians(round(car.angle)))


    def rear_beam(self, car):
        self.position_rear_beam.x = car.position.x - self.rear_beam_distance * cos(radians(round(car.angle)))
        self.position_rear_beam.y = car.position.y + self.rear_beam_distance * sin(radians(round(car.angle)))

    
    def update(self, car):

        self.low_beam(car)
        self.high_beam(car)
        self.blink_right(car)
        self.blink_left(car)
        self.rear_beam(car)