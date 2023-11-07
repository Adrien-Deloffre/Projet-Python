__author__ = ["adrien_deloffre"]

""" the World class spawn building, pedestrian crossing and pedestrian on the map, it also fill the different obstacles lists """

import pygame

class World():

    def __init__(self):
        
        pygame.display.set_caption("Simulateur vehicule autonome")
        self.WIDTH_SCREEN = 1550
        self.HEIGHT_SCREEN = 1050
        self.screen = pygame.display.set_mode((self.WIDTH_SCREEN, self.HEIGHT_SCREEN))

        # Color initialisation
        self.WHITE = pygame.Color(255, 255, 255)
        self.RED = pygame.Color(255, 0, 0)
        self.BLUE = pygame.Color(0, 0, 100)
        self.GREEN = pygame.Color(0, 155, 0)
        self.GRAY = pygame.Color(50, 50, 50)

        self.WIDHT_ROAD = 150
        self.WIDTH_BUILDING = 200
        self.HEIGHT_BUILDING = 150
        self.WIDHT_SIDEWALK = 60
        self.HEIGHT_SIDEWALK = 20

        self.obstacle_list = []
        self.pedestrian_crossing_list = []
        self.signage_list = []
        self.complete_list = []


    def horizontal_pedestrian_crossing(self, x, y, w, h):
        pygame.draw.rect(self.screen, self.BLUE, (x+20, y, w, h))
        pygame.draw.rect(self.screen, self.BLUE, (x+60, y, w, h))
        pygame.draw.rect(self.screen, self.BLUE, (x+100, y, w, h))


    def vertical_pedestrian_crossing(self, x, y, w, h):
        pygame.draw.rect(self.screen, self.BLUE, (x, y+20, w, h))
        pygame.draw.rect(self.screen, self.BLUE, (x, y+60, w, h))
        pygame.draw.rect(self.screen, self.BLUE, (x, y+100, w, h))


    def draw(self, color, building):
        pygame.draw.rect(self.screen, color, (building.left, building.top, building.width, building.height))


    def run(self):

        # road
        pygame.draw.rect(self.screen, self.WHITE, (0, 0, self.WIDTH_SCREEN, self.HEIGHT_SCREEN))

        # building
        building_1 = pygame.Rect(150, 150, 200, 150)
        building_2 = pygame.Rect(0, 450, 350, 150)
        building_3 = pygame.Rect(150, 750, 200, 150)
        building_4 = pygame.Rect(500, 150, 200, 750)
        building_5 = pygame.Rect(850, 0, 200, 300)
        building_6 = pygame.Rect(850, 450, 350, 150)
        building_7 = pygame.Rect(850, 750, 200, 300)
        building_8 = pygame.Rect(1200, 150, 200, 450)
        building_9 = pygame.Rect(1200, 750, 200, 150)
        # draw building
        self.draw(self.GRAY, building_1)
        self.draw(self.GRAY, building_2)
        self.draw(self.GRAY, building_3)
        self.draw(self.GRAY, building_4)
        self.draw(self.GRAY, building_5)
        self.draw(self.GRAY, building_6)
        self.draw(self.GRAY, building_7)
        self.draw(self.GRAY, building_8)
        self.draw(self.GRAY, building_9)

        # window border (create rectangle for obstacle detection in the window edges)
        border_1 = pygame.Rect(0, -200, self.WIDTH_SCREEN+200, 200)
        border_2 = pygame.Rect(self.WIDTH_SCREEN, 0, 200, self.HEIGHT_SCREEN+200)
        border_3 = pygame.Rect(0, self.HEIGHT_SCREEN, self.WIDTH_SCREEN, 200)
        border_4 = pygame.Rect(-200, -200, 200, self.HEIGHT_SCREEN+400)

        # pedestrian crossing
        pedestrian_crossing_1 = self.horizontal_pedestrian_crossing(self.WIDHT_ROAD+self.WIDTH_BUILDING, self.WIDHT_ROAD, self.HEIGHT_SIDEWALK, self.WIDHT_SIDEWALK)
        pedestrian_crossing_2 = self.horizontal_pedestrian_crossing(self.WIDHT_ROAD+self.WIDTH_BUILDING, 2*self.WIDHT_ROAD+self.HEIGHT_BUILDING, self.HEIGHT_SIDEWALK, self.WIDHT_SIDEWALK)
        pedestrian_crossing_3 = self.vertical_pedestrian_crossing(self.WIDHT_ROAD+140, 2*self.WIDHT_ROAD+2*self.HEIGHT_BUILDING, self.WIDHT_SIDEWALK, self.HEIGHT_SIDEWALK)
        pedestrian_crossing_4 = self.vertical_pedestrian_crossing(3*self.WIDHT_ROAD+2*self.WIDTH_BUILDING, self.WIDHT_ROAD+self.HEIGHT_BUILDING, self.WIDHT_SIDEWALK, self.HEIGHT_SIDEWALK)
        # delimitation of the pedestrian crossing to simplify detection (draw a rectangle around the pedestrian crossing)
        rect_pedestrian_crossing_1 = pygame.Rect(self.WIDHT_ROAD+self.WIDTH_BUILDING, self.WIDHT_ROAD-10, self.WIDHT_ROAD, self.WIDHT_SIDEWALK+20)
        rect_pedestrian_crossing_2 = pygame.Rect(self.WIDHT_ROAD+self.WIDTH_BUILDING, 2*self.WIDHT_ROAD+self.HEIGHT_BUILDING-10, self.WIDHT_ROAD, self.WIDHT_SIDEWALK+20)
        rect_pedestrian_crossing_3 = pygame.Rect(self.WIDHT_ROAD+140-10, 2*self.WIDHT_ROAD+2*self.HEIGHT_BUILDING, self.WIDHT_SIDEWALK+20, self.WIDHT_ROAD)
        rect_pedestrian_crossing_4 = pygame.Rect(3*self.WIDHT_ROAD+2*self.WIDTH_BUILDING-10, self.WIDHT_ROAD+self.HEIGHT_BUILDING, self.WIDHT_SIDEWALK+20, self.WIDHT_ROAD)
        pygame.draw.rect(self.screen, self.RED, rect_pedestrian_crossing_1,1)
        pygame.draw.rect(self.screen, self.RED, rect_pedestrian_crossing_2,1)
        pygame.draw.rect(self.screen, self.RED, rect_pedestrian_crossing_3,1)
        pygame.draw.rect(self.screen, self.RED, rect_pedestrian_crossing_4,1)
        
        # pedestrian
        pedestrian_image = pygame.image.load("img/pedestrian.png")
        self.screen.blit(pedestrian_image, (280, 600))
        rect_pedestrian = pedestrian_image.get_rect()
        # delimitation of the pedestrian to simplify detection (draw a rectangle around the pedestrian)
        pedestrian = pygame.Rect(280, 600, rect_pedestrian.width, rect_pedestrian.height)
        pygame.draw.rect(self.screen, self.RED, pedestrian,1)

        # visual signage to indicate crossroad
        signage_1 = pygame.Rect(350, 0, 150, 150)
        signage_2 = pygame.Rect(350, 300, 150, 150)
        signage_3 = pygame.Rect(350, 600, 150, 150)
        signage_4 = pygame.Rect(350, 900, 150, 150)
        signage_5 = pygame.Rect(700, 300, 150, 150)
        signage_6 = pygame.Rect(700, 600, 150, 150)
        signage_7 = pygame.Rect(1050, 600, 150, 150)
        signage_8 = pygame.Rect(1400, 600, 150, 150)
        # delimitation of the crossroad
        pygame.draw.rect(self.screen, self.GREEN, signage_1,1)
        pygame.draw.rect(self.screen, self.GREEN, signage_2,1)
        pygame.draw.rect(self.screen, self.GREEN, signage_3,1)
        pygame.draw.rect(self.screen, self.GREEN, signage_4,1)
        pygame.draw.rect(self.screen, self.GREEN, signage_5,1)
        pygame.draw.rect(self.screen, self.GREEN, signage_6,1)
        pygame.draw.rect(self.screen, self.GREEN, signage_7,1)
        pygame.draw.rect(self.screen, self.GREEN, signage_8,1)

        #######################################################################  fill lists of different obstacles  #########################################################################

        self.obstacle_list = [building_1, building_2, building_3, building_4, building_5, building_6, building_7, building_8, building_9, border_1, border_2, border_3, border_4, pedestrian]
        self.pedestrian_crossing_list = [rect_pedestrian_crossing_1, rect_pedestrian_crossing_2, rect_pedestrian_crossing_3, rect_pedestrian_crossing_4]
        self.signage_list = [signage_1, signage_2, signage_3, signage_4, signage_5, signage_6, signage_7, signage_8]
        self.complete_list = [self.obstacle_list, self.pedestrian_crossing_list, self.signage_list]