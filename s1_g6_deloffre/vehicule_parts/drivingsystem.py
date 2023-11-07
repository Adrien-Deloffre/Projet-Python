__author__ = ["adrien_deloffre"]

""" the Drivingsystem class manage the vehicle movement capacity """

from math import sin, cos, radians, degrees
from pygame.math import Vector2

class Drivinsystem():

    def __init__(self, x, y, angle=0.0, length=4, max_steering=60, max_acceleration=2.0):

        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)

        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 4
        self.brake_deceleration = 10
        self.free_deceleration = 2
        self.min_rpm =1200

        self.acceleration = 0.0
        self.steering = 0.0
        self.gear = 0
        self.rpm = 0

    def update(self, dt):
        
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        ############################ gear box

        if self.velocity.x < 0:
            self.gear = -1
        if self.velocity.x > 0 and self.velocity.x < 1.5:
            self.gear = 1
        if self.velocity.x > 1.5 and self.velocity.x < 3.5:
            self.gear = 2
        if self.velocity.x > 3.5 and self.velocity.x < 10:
            self.gear = 3

        ############################ engine speed

        if self.velocity.x == 0:
            self.rpm = self.min_rpm
            self.gear = 0
        else:
            self.rpm = self.min_rpm + round((self.velocity.x*1000)/self.gear)

        ############################

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt