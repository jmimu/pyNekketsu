# -*- coding: utf-8 -*-
#! /usr/bin/python

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


