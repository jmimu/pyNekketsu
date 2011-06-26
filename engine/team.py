#! /usr/bin/python
# -*- coding: utf-8 -*-

#    pyNekketsu
#    Copyright (C) 2011  JM Muller
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pygame
import os
from perso_cpu import PersoCPU
from perso_GK import Perso_GK
import random


#number of differents heads 
nbr_heads=3


#
class Team(object):
    def __init__(self, number, img_team, name_team, wing, field, nb_players_cpu):#wing where they look: -1 (west) or +1 (east)
        self.number=number
        self.image=pygame.image.load(img_team)
        self.name=name_team
        self.nb_goals=0
        self.wing=wing #wing for target, -wing for own goal
        self.persos=[]
        self.persos_ordered_dist_to_ball=[]
        #add the GK
        self.persos.append(Perso_GK(self,random.randint(1, nbr_heads), [-self.wing*field.half_length, field.goal_latitude[-self.wing],0 ]))
        #add the other players
        for i in range(nb_players_cpu):
            self.persos.append(PersoCPU(self,random.randint(1, nbr_heads),[-self.wing*field.half_length*((i+1.0)/(nb_players_cpu+2.0)), field.goal_latitude[-self.wing],0 ]))
    
        self.persos_ordered_dist_to_ball[:]=self.persos[1:]
    
    def update(self,match):
        for p in self.persos:
            p.update(match)

        self.persos_ordered_dist_to_ball=sorted( self.persos_ordered_dist_to_ball,   key=lambda Perso: Perso.dist2_to_ball) #sort all the perses list with dist2_to_ball

