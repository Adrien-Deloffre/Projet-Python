__author__ = ["adrien_deloffre"]

""" main of the game  """

import pygame
import random
from math import copysign

from world import World
from vehicule import Vehicule
from canbus import CanBus


class Simulation:

    def __init__(self):

        pygame.init()

        ############################ define time element
    
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.frame_count = 0
        self.total_seconds = 0
        self.exit = False

        ############################ other definition

        self.numero_design = 2
        self.bool_low_beam = False
        self.bool_high_beam = False
        self.bool_autonomous = False

    def run(self):

        ############################ Class initialisation

        world = World()
        car = Vehicule()
        can = CanBus()

        ############################

        ppu = 32

        while not self.exit:

            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            ############################ time gestion
            # Calculate total seconds
            self.total_seconds = self.frame_count // self.ticks
            # Divide by 60 to get total minutes
            minutes = self.total_seconds // 60
            # Use modulus (remainder) to get seconds
            seconds = self.total_seconds % 60

            ############################ screen display the map
            self.screen = world.screen
            world.run()

            ############################ game

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_a]:
                self.bool_autonomous = not self.bool_autonomous

            ############################################################# manual control ############################################################

            if self.bool_autonomous == False:

                if pressed[pygame.K_UP]:
                    if car.drivingsystem.velocity.x < 0:
                        car.drivingsystem.acceleration = car.drivingsystem.brake_deceleration
                    else:
                        car.drivingsystem.acceleration += 1 * dt
                elif pressed[pygame.K_DOWN]:
                    if car.drivingsystem.velocity.x > 0:
                        car.drivingsystem.acceleration = -car.drivingsystem.brake_deceleration
                    else:
                        car.drivingsystem.acceleration -= 1 * dt
                else:
                    if abs(car.drivingsystem.velocity.x) > dt * car.drivingsystem.free_deceleration:
                        car.drivingsystem.acceleration = -copysign(car.drivingsystem.free_deceleration, car.drivingsystem.velocity.x)
                    else:
                        if dt != 0:
                            car.drivingsystem.acceleration = -car.drivingsystem.velocity.x / dt
                car.drivingsystem.acceleration = max(-car.drivingsystem.max_acceleration, min(car.drivingsystem.acceleration, car.drivingsystem.max_acceleration))

                if pressed[pygame.K_RIGHT]:
                    car.drivingsystem.steering -= 40 * dt
                elif pressed[pygame.K_LEFT]:
                    car.drivingsystem.steering += 40 * dt
                else:
                    car.drivingsystem.steering = 0

            ############################################################# autonomous mode ############################################################

            if self.bool_autonomous == True:
                car.drivingsystem.acceleration += 1 * dt

                if car.sensing.image_segmentation.front_collision == False and car.sensing.image_segmentation.turn_right == False and  car.sensing.image_segmentation.turn_left == False:
                    car.drivingsystem.steering = 0

                if car.sensing.image_segmentation.front_collision == True and car.sensing.image_segmentation.touch_right == True:
                    car.drivingsystem.steering += 60 

                if car.sensing.image_segmentation.front_collision == True and car.sensing.image_segmentation.touch_left == True:
                    car.drivingsystem.steering -= 60

                if car.sensing.image_segmentation.crossroad == False and car.sensing.image_segmentation.touch_right == True:
                    car.drivingsystem.steering += 60

                if car.sensing.image_segmentation.crossroad == False and car.sensing.image_segmentation.touch_left == True:
                    car.drivingsystem.steering -= 60

                if seconds<30:
                    left_or_right = 0 # 0 --> left
                else:
                    left_or_right = 1 # 1 --> right

                if car.sensing.image_segmentation.crossroad == True:
                    if left_or_right == 0 and car.sensing.image_segmentation.touch_left == False:
                        car.drivingsystem.steering += 60
                        rotated = pygame.transform.rotate(car.lighting.left_blink_image, car.drivingsystem.angle)
                        rect_left_blink = rotated.get_rect()
                        can.send(0xad, [1,2,3])
                        # blink
                        if self.frame_count % 15 == 1:
                            self.screen.blit(rotated, car.lighting.position_left_blink * ppu - (rect_left_blink.width / 2, rect_left_blink.height / 2))
            
                    if left_or_right == 1 and car.sensing.image_segmentation.touch_right == False:
                        car.drivingsystem.steering -= 60
                        rotated = pygame.transform.rotate(car.lighting.right_blink_image, car.drivingsystem.angle)
                        rect_right_blink = rotated.get_rect()
                        can.send(0xad, [1,2,4])
                        # blink
                        if self.frame_count % 15 == 1:
                            self.screen.blit(rotated, car.lighting.position_right_blink * ppu - (rect_right_blink.width / 2, rect_right_blink.height / 2))

                # pedestrian crossing (slow down)
                if car.sensing.image_segmentation.pedestrian_crossing == True:
                    car.drivingsystem.acceleration = -car.drivingsystem.free_deceleration
                
            ############################################################# default setting ############################################################
            # if all front sensors collide, need to back up
            if car.sensing.image_segmentation.front_collision == True and car.sensing.image_segmentation.turn_right == True and  car.sensing.image_segmentation.turn_left == True:
                car.drivingsystem.acceleration = -car.drivingsystem.brake_deceleration
            # if rear sensor collide, need to move forward
            if car.sensing.image_segmentation.rear_collision == True:
                car.drivingsystem.acceleration = car.drivingsystem.brake_deceleration

            # obligation to turn if bool turn_right or turn_left are TRUE 
            if car.sensing.image_segmentation.front_collision == True and car.sensing.image_segmentation.turn_right == True:
                car.drivingsystem.steering -= 55
            if car.sensing.image_segmentation.front_collision == True and car.sensing.image_segmentation.turn_left == True:
                car.drivingsystem.steering += 55
            if car.sensing.image_segmentation.turn_right == True and car.sensing.image_segmentation.rear_collision == False:
                car.drivingsystem.steering -= 20
            if car.sensing.image_segmentation.turn_left == True and car.sensing.image_segmentation.rear_collision == False:
                car.drivingsystem.steering += 20

            car.drivingsystem.steering = max(-car.drivingsystem.max_steering, min(car.drivingsystem.steering, car.drivingsystem.max_steering))

            car.update(dt, self.numero_design, car, world.complete_list)
            
            # envoi dans le bus can la distance a "front ranger" en continue
            # can.send(0xae, round(car.sensing.ranger.front_distance))

            ############################################################# Drawing #####################################################################

            #self.screen.fill((255, 255, 255))
            font=pygame.font.Font(None, 24)

            ############################ car design (choose the different design of car by pressing the key "F1", "F2", "F3" ou "F4)

            if pressed[pygame.K_F1]:
                self.numero_design = 1

            if pressed[pygame.K_F2]:
                self.numero_design = 2

            if pressed[pygame.K_F3]:
                self.numero_design = 3

            if pressed[pygame.K_F4]:
                self.numero_design = 4

            rotated = pygame.transform.rotate(car.design.car_image, car.drivingsystem.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.drivingsystem.position * ppu - (rect.width / 2, rect.height / 2))

            ############################ display the sensors around the car
            # front collision rectangle
            pygame.draw.rect(self.screen, pygame.Color(255, 0, 0), (car.sensing.image_segmentation.position_front_radar.x, car.sensing.image_segmentation.position_front_radar.y, 5, 5), 1)
            # rear collision rectangle
            pygame.draw.rect(self.screen, pygame.Color(255, 0, 0), (car.sensing.image_segmentation.position_rear_radar.x, car.sensing.image_segmentation.position_rear_radar.y, 5, 5), 1)
            # front right collision rectangle
            pygame.draw.rect(self.screen, pygame.Color(255, 0, 0), (car.sensing.image_segmentation.position_front_right_radar.x, car.sensing.image_segmentation.position_front_right_radar.y, 5, 5), 1)
            # front left collision rectangle
            pygame.draw.rect(self.screen, pygame.Color(255, 0, 0), (car.sensing.image_segmentation.position_front_left_radar.x, car.sensing.image_segmentation.position_front_left_radar.y, 5, 5), 1)
            # right collision rectangle
            pygame.draw.rect(self.screen, pygame.Color(255, 0, 0), (car.sensing.image_segmentation.position_right_radar.x, car.sensing.image_segmentation.position_right_radar.y, 5, 5), 1)
            # left collision rectangle
            pygame.draw.rect(self.screen, pygame.Color(255, 0, 0), (car.sensing.image_segmentation.position_left_radar.x, car.sensing.image_segmentation.position_left_radar.y, 5, 5), 1)
            # front lidar rectangle
            pygame.draw.rect(self.screen, pygame.Color(0, 255, 0), (car.sensing.ranger.position_front_lidar.x, car.sensing.ranger.position_front_lidar.y, 2, 2), 1)

            ############################ headlight (when you clic on the touch L or H of the keyboard, the boolean "bool_low_beam" or "bool_hight_beam"
            ############################ change of value and turn on or turn off the low beam or the hight beam according to their previous value)

            if pressed[pygame.K_l]:
                self.bool_low_beam = not self.bool_low_beam
                can.send(0xac, [1,2,3])
            if self.bool_low_beam == True:
                rotated = pygame.transform.rotate(car.lighting.low_beam_image, car.drivingsystem.angle)
                rect_low_beam = rotated.get_rect()
                self.screen.blit(rotated, car.lighting.position_low_beam * ppu - (rect_low_beam.width / 2, rect_low_beam.height / 2))
            
            if pressed[pygame.K_h]:
                self.bool_high_beam = not self.bool_high_beam
                can.send(0xac, [1,2,4])
            if self.bool_high_beam == True:
                rotated = pygame.transform.rotate(car.lighting.high_beam_image, car.drivingsystem.angle)
                rect_high_beam = rotated.get_rect()
                self.screen.blit(rotated, car.lighting.position_high_beam * ppu - (rect_high_beam.width / 2, rect_high_beam.height / 2))

            ############################ turn signal (when you clic on the touch --> or <-- of the keyboard)

            if pressed[pygame.K_RIGHT]:
                if self.frame_count % 15 == 1:
                    rotated = pygame.transform.rotate(car.lighting.right_blink_image, car.drivingsystem.angle)
                    rect_right_blink = rotated.get_rect()
                    self.screen.blit(rotated, car.lighting.position_right_blink * ppu - (rect_right_blink.width / 2, rect_right_blink.height / 2))

            if pressed[pygame.K_LEFT]:
                if self.frame_count % 15 == 1:
                    rotated = pygame.transform.rotate(car.lighting.left_blink_image, car.drivingsystem.angle)
                    rect_left_blink = rotated.get_rect()
                    self.screen.blit(rotated, car.lighting.position_left_blink * ppu - (rect_left_blink.width / 2, rect_left_blink.height / 2))

            ############################ distance between the car and the nearest obstacle in front (from Ranger class)

            text_front_distance_value = font.render(str(round(car.sensing.ranger.front_distance,1)),1,(0,0,0))
            self.screen.blit(text_front_distance_value, car.lighting.position_low_beam * ppu)

            ############################ information of collision (from ImageSegmentation class)

            if car.sensing.image_segmentation.front_collision == True:
                text_collision_value = font.render("OBSTACLE",1,(255,0,0))
                self.screen.blit(text_collision_value, (600 , 20))

            if car.sensing.image_segmentation.pedestrian_crossing == True:
                text_pedestrian_crossing_value = font.render("PASSAGE PIETON",1,(255,0,0))
                self.screen.blit(text_pedestrian_crossing_value, (750 , 20))

            ############################ information to display on the side of the game screen

            # time of game
            time_value = "Time: {0:02}:{1:02}".format(minutes, seconds)
            text_time = font.render(time_value, True, (0,0,0))
            self.screen.blit(text_time, (10, 10))

            # car speed
            text_speed = font.render("vitesse : ",1,(0,0,0))
            text_speed_value = font.render(str(round(car.drivingsystem.velocity.x*10)),1,(0,0,0))
            self.screen.blit(text_speed, (world.WIDTH_SCREEN - 220 , 10))
            self.screen.blit(text_speed_value, (world.WIDTH_SCREEN - 100 , 10))

            # car rpm
            text_rpm = font.render("tours/minute : ",1,(0,0,0))
            text_rpm_value = font.render(str(car.drivingsystem.rpm),1,(0,0,0))
            self.screen.blit(text_rpm, (world.WIDTH_SCREEN - 220 , 30))
            self.screen.blit(text_rpm_value, (world.WIDTH_SCREEN - 100 , 30))

            # gearbox report
            text_gear = font.render("rapport : ",1,(0,0,0))
            text_gear_value = font.render(str(car.drivingsystem.gear),1,(0,0,0))
            self.screen.blit(text_gear, (world.WIDTH_SCREEN - 220 , 50))
            self.screen.blit(text_gear_value, (world.WIDTH_SCREEN - 100 , 50))

            # headlight turn on or turn off
            text_beam = font.render("phare : ",1,(0,0,0))
            if self.bool_low_beam == True or self.bool_high_beam == True:
                text_beam_value = font.render("allumé",1,(0,0,0))
            else:
                text_beam_value = font.render("éteint",1,(0,0,0))
            self.screen.blit(text_beam, (world.WIDTH_SCREEN - 200 , world.HEIGHT_SCREEN - 50))
            self.screen.blit(text_beam_value, (world.WIDTH_SCREEN - 100 , world.HEIGHT_SCREEN - 50))

            # canbus
            text_can = font.render("dernier message sur le bus can : ",1,(0,0,0))
            message_can = font.render(can.message,1,(0,0,0))
            self.screen.blit(text_can, (10 , world.HEIGHT_SCREEN - 50))
            self.screen.blit(message_can, (300 , world.HEIGHT_SCREEN - 50))

            # autonomy
            if self.bool_autonomous == True:
                text_mode = font.render("MODE AUTONOME",1,(255,0,0))
            else:
                text_mode = font.render("MODE MANUEL",1,(255,0,0))
            self.screen.blit(text_mode, (world.WIDTH_SCREEN/2 - 80 , world.HEIGHT_SCREEN -50))

            #############################################################################################################################################################

            self.frame_count +=1
            self.clock.tick(self.ticks)

            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    simulation = Simulation()
    simulation.run()