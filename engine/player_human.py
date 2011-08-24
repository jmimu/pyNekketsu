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
from player_non_GK import Player_non_GK
from inputs import Inputs

class Player_Human(Player_non_GK):
    
    def __init__(self,team,num_player=1,num_player_image_name="data/1.png"):
        Player_non_GK.__init__(self,team)
        self.inputs=Inputs(num_player) #key config: player num_player
        self.num_player_image=pygame.image.load(num_player_image_name)
        self.number_human_player=num_player
        
    def update(self,match):
        Player_non_GK.update(self,match) 
        
    def draw(self,surface,camera,is_shadow=True):
        Player_non_GK.draw(self,surface,camera,is_shadow)
        projection=camera.proj([self.pos[0],self.pos[1],self.pos[2]],self.team.image.get_width(),self.team.image.get_height()*0)
        surface.blit(self.num_player_image, camera.proj([self.pos[0],self.pos[1],self.pos[2]],self.team.image.get_width(),self.team.image.get_height()*0))
        has_to_draw_arrow=False
        if (projection[0]>256-self.num_player_image.get_width()):
            projection[0]=256-self.num_player_image.get_width()
            has_to_draw_arrow=True
        if (projection[0]<0):
            projection[0]=0
            has_to_draw_arrow=True
        if (projection[1]>240-self.team.image.get_height()*1):
            projection[1]=240-self.num_player_image.get_height()*1
            has_to_draw_arrow=True
        if (projection[1]<0):
            projection[1]=0
            has_to_draw_arrow=True
        
        if (has_to_draw_arrow):
            surface.blit(self.num_player_image, projection)
        


