__author__ = ["adrien_deloffre"]

""" the Design class allows you to load different vehicule designs """

import pygame

class Design():

    def __init__(self):
        self.car_image = pygame.image.load("img/car2.png")

    def update(self, numero):
        if numero == 1:
            self.car_image = pygame.image.load("img/car.png")
        if numero == 2:
            self.car_image = pygame.image.load("img/car2.png")
        if numero == 3:
            self.car_image = pygame.image.load("img/car3.png")
        if numero == 4:
            self.car_image = pygame.image.load("img/car4.png")