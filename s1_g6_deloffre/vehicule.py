__author__ = ["adrien_deloffre"]

from vehicule_parts.design import Design
from vehicule_parts.sensing import Sensing
from vehicule_parts.lighting import Lighting
from vehicule_parts.drivingsystem import Drivinsystem


class Vehicule():

    def __init__(self):
        
        self.drivingsystem = Drivinsystem(5, 2)
        self.lighting = Lighting()
        self.sensing = Sensing()
        self.design = Design()


    def update(self, dt ,numero_design, car, elementlist):
        
        self.drivingsystem.update(dt)
        self.lighting.update(car.drivingsystem)
        self.sensing.update(car.drivingsystem, elementlist)
        self.design.update(numero_design)