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
import random
from perso import Perso
from inputs import Inputs



class PersoCPU(Perso):
    difficulty=8 #out of 10
    def __init__(self,team,head):
        Perso.__init__(self,team,head)
        self.inputs=Inputs(0)
        
    def update(self,match):
        Perso.update(self,match) 
#        self.think(match)

    def think(self,match):#press on virtual keys
        if (self.has_ball!=0):
            #look in the goal's direction
            if (self.team.wing==1):
                self.inputs.R=True
            else:
                self.inputs.L=True
            if (match.field.goal_latitude[self.team.wing]-10>self.pos[1]) or (random.randint(0, 4)==0):
                self.inputs.U=True
            if (match.field.goal_latitude[self.team.wing]+10<self.pos[1]) or (random.randint(0, 4)==0):
                self.inputs.D=True
            #shoot!
            if (random.randint(0, int(abs(self.team.wing*match.field.half_length-self.pos[0])))==0):#depends on the distance to the goal
                self.inputs.B=True
        else:
            if (self.pos[0]<match.ball.pos[0]-2) and (random.randint(0, 20)<10+PersoCPU.difficulty):
                self.inputs.R=True
            if (self.pos[0]>match.ball.pos[0]+2) and (random.randint(0, 20)<10+PersoCPU.difficulty):
                self.inputs.L=True
            if (self.pos[1]<match.ball.pos[1]-5) and (random.randint(0, 20)<10+PersoCPU.difficulty):
                self.inputs.U=True
            if (self.pos[1]>match.ball.pos[1]+5) and (random.randint(0, 20)<10+PersoCPU.difficulty):
                self.inputs.D=True
            for p in match.perso_list:
                if (p!=self):
                    if (p.team!=self.team):#attack!
                        if (abs(p.pos[0]-self.pos[0])<6 and abs(p.pos[1]-self.pos[1])<6):
                            if (random.randint(0, 80)==0) or (p.has_ball!=0):
                                self.inputs.A=True


