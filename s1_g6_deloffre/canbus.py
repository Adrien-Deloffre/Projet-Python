__author__ = ["adrien_deloffre"]

""" the CanBus class generates and sends can frames """

import pygame
import can

class CanBus():

    def __init__(self):

        # create a bus instance
        self.bus_1 = can.interface.Bus('channel_1', bustype='virtual')
        self.bus_2 = can.interface.Bus('channel_1', bustype='virtual')

        self.message = "pas de message"


    def send(self, id_value, data_value):

        msg1 = can.Message(arbitration_id=id_value, data=data_value)
        self.bus_1.send(msg1)

        msg2 = self.bus_2.recv()

        if msg2.arbitration_id == 0xac:
            if msg2.data[2] == 3:
                self.message = "commande feux de croisement"
            if msg2.data[2] == 4:
                self.message = "commande feux de route"
        if msg2.arbitration_id == 0xad:
            if msg2.data[2] == 3:
                self.message = "commande clignotant gauche"
            if msg2.data[2] == 4:
                self.message = "commande clignotant droit"
