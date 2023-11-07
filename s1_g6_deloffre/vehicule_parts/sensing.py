__author__ = ["adrien_deloffre"]

import pygame

from vehicule_parts.sensing_devices.ranger import Ranger
from vehicule_parts.sensing_devices.imagesegmentation import ImageSegmentation

class Sensing():

    def __init__(self):

        self.image_segmentation = ImageSegmentation()
        self.ranger = Ranger()

    def update(self, car, elementlist):

        self.image_segmentation.update(car, elementlist)
        self.ranger.update(car, elementlist)