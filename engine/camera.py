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

import pygame,sys

from pygame.locals import *
from field import Field

#to draw everything in field world, with a projection

class Camera():
    def __init__(self,field):
        self.field=field #to have limitations
        self.x=0.0#camera position
        self.y=-100.0
        self.z=0.0
        self.f=550.0#camera focale
        self.l=-50#120 #center of the screen, or less to fake a little tilt
        self.c=128 #center of the screen
        self.decal_to_target=[0,-150,50]
    def aim_to(self,ground_pos,direction,speed=100): # try to go closer to ground_pos point, and look forward in a direction , at a given speed (in %)
        self.decal_to_target[0]=25.0*direction#add to x
        self.x+=(ground_pos[0]+self.decal_to_target[0]-self.x)*speed/100.0
        self.y+=(ground_pos[1]+self.decal_to_target[1]-self.y)*speed/100.0
        self.z+=(ground_pos[2]+self.decal_to_target[2]-self.z)*speed/100.0
        if (self.x<-self.field.half_length+20):
            self.x=-self.field.half_length+20
        if (self.x>self.field.half_length-20):
            self.x=self.field.half_length-20
    def proj(self,ground_pos,sprite_w=0,sprite_h=0):#ground_pos is a 3D vector
        px=ground_pos[0]-self.x
        py=ground_pos[1]-self.y
        pz=ground_pos[2]-self.z
        pc=px/py*self.f+self.c  -sprite_w/2
        pl=-pz/py*self.f+self.l  -sprite_h
        screen_pos=[pc,pl]
        return screen_pos

