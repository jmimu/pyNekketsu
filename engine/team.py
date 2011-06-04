#! /usr/bin/python


import pygame
import os
from perso_cpu import PersoCPU

#
class Team(object):
    def __init__(self, img_team, name_team, wing, nb_players_cpu):#wing: -1 (west) or +1 (east)
        self.image=pygame.image.load(img_team)
        self.name=name_team
        self.nb_goals=0
        self.wing=wing
        self.persos=[]
        for i in range(nb_players_cpu):
            self.persos.append(PersoCPU(self))


