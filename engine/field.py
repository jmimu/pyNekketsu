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

from settings import configuration
from sprite import coloringimage

#Field represents the soccer field: size, drawing, goal position...

class Field():
    sky_image=pygame.image.load("data/sky.png")
    grass_image=pygame.image.load("data/grass.png")
    
    
    def __init__(self,west_top_color,west_bottom_color,east_top_color,east_bottom_color):
        self.half_length=100
        self.half_width=50
        self.z=0.0
        
        self.goal_half_width={}#-1: west goal, +1: east goal
        self.goal_height={}
        self.goal_latitude={}
        
        self.goal_half_width[-1]=22#west goal
        self.goal_height[-1]=15
        self.goal_latitude[-1]=0#where the goal center is inside field width
        self.goal_half_width[1]=22#east goal
        self.goal_height[1]=15
        self.goal_latitude[1]=0#where the goal center is inside field width
        self.bounce_damp=0.6#1=perfect
        self.roll_damp=0.9#1=perfect
        
        self.flag_back_image_west=coloringimage("../flag_back.png",west_top_color,west_bottom_color)
        self.flag_front_image_west=coloringimage("../flag_front.png",west_top_color,west_bottom_color)
        self.flag_back_image_east=coloringimage("../flag_back.png",east_top_color,east_bottom_color)
        self.flag_front_image_east=coloringimage("../flag_front.png",east_top_color,east_bottom_color)

    def collide_with_player(self,player): #block a player inside the field
        # If we're at ground level, stop.
        if (player.pos[2] <= self.z):
            player.pos[2] = self.z
            player.jump_speed = 0
            if (player.state=="jump"):
                player.state="walk"
                player.anim_index=0
                player.previous_pos[:]=player.pos[:]
        
        # Keep the player in bounds
        if player.pos[0] < -self.half_length:
            player.pos[0] = -self.half_length
        if player.pos[0] > self.half_length:
            player.pos[0] = self.half_length
        if player.pos[1] < -self.half_width:
            player.pos[1] = -self.half_width
        if player.pos[1] > self.half_width:
            player.pos[1] = self.half_width


    def draw(self,surface,camera):
        #background
        tmp,horizon_y=camera.proj([0,500,self.z])
        horizon_y=horizon_y+80
        horizon_x,tmp=camera.proj([0,1000,self.z])
        surface.blit(Field.sky_image,(horizon_x-Field.sky_image.get_width()/2,horizon_y-Field.sky_image.get_height()))
        #pygame.draw.rect(surface, ( 200, 200, 255), (0, 0,256,horizon_y))
        #pygame.draw.rect(surface, ( 13, 83,  19), (0, horizon_y, 256, 241-horizon_y))
        surface.blit(Field.grass_image,(0,horizon_y))
        #pygame.draw.rect(surface, (255, 200, 185), (0, horizon_y+2, 256,  1), 1)
        
        #hz lines
        #for x in range(11):
        #    pygame.draw.line(surface, (185, 200, 105), camera.proj([-self.half_length+x*20,-self.half_width,self.z]), camera.proj([-self.half_length+x*20,self.half_width,self.z]), 1)
        #for y in range(6):
        #    pygame.draw.line(surface, (185, 200, 105), camera.proj([-self.half_length,-self.half_width+y*20,self.z]), camera.proj([self.half_length,-self.half_width+y*20,self.z]), 1)
        pygame.draw.line(surface, (225, 230, 255), camera.proj([-self.half_length,-self.half_width,self.z]), camera.proj([-self.half_length,self.half_width,self.z]), 3)
        pygame.draw.line(surface, (225, 230, 255), camera.proj([-self.half_length,self.half_width,self.z]), camera.proj([self.half_length,self.half_width,self.z]), 3)
        pygame.draw.line(surface, (225, 230, 255), camera.proj([self.half_length,self.half_width,self.z]), camera.proj([self.half_length,-self.half_width,self.z]), 3)
        pygame.draw.line(surface, (225, 230, 255), camera.proj([self.half_length,-self.half_width,self.z]), camera.proj([-self.half_length,-self.half_width,self.z]), 3)
        pygame.draw.line(surface, (225, 230, 255), camera.proj([0,self.half_width,self.z]), camera.proj([0,-self.half_width,self.z]), 3)
     
        #draw back flags
        pos=camera.proj([self.half_length,self.half_width,self.z+8])
        pos[1]-=8
        pygame.draw.line(surface, (180, 180, 185), camera.proj([self.half_length,self.half_width,self.z]),pos, 2)
        surface.blit(self.flag_back_image_east,pos)
        pos=camera.proj([-self.half_length,self.half_width,self.z+8])
        pos[1]-=8
        pygame.draw.line(surface, (180, 180, 185), camera.proj([-self.half_length,self.half_width,self.z]),pos, 2)
        surface.blit(self.flag_back_image_west,pos)
        
     
        if (configuration["game_mode"]!="fight"):
            #goals
            pygame.draw.line(surface, (245, 180, 165), camera.proj([-self.half_length,self.goal_latitude[-1]-self.goal_half_width[-1],self.z+self.goal_height[-1]]),
               camera.proj([-self.half_length,self.goal_latitude[-1]+self.goal_half_width[-1],self.z+self.goal_height[-1]]), 5)
            pygame.draw.line(surface, (245, 180, 165), camera.proj([-self.half_length,self.goal_latitude[-1]-self.goal_half_width[-1],self.z]),
               camera.proj([-self.half_length,self.goal_latitude[-1]-self.goal_half_width[-1],self.z+self.goal_height[-1]]), 5)
            pygame.draw.line(surface, (245, 180, 165), camera.proj([-self.half_length,self.goal_latitude[-1]+self.goal_half_width[-1],self.z]),
               camera.proj([-self.half_length,self.goal_latitude[-1]+self.goal_half_width[-1],self.z+self.goal_height[-1]]), 5)

            pygame.draw.line(surface, (225, 230, 255), camera.proj([-self.half_length,self.goal_latitude[-1]+self.goal_half_width[-1],self.z]),
               camera.proj([-self.half_length+20,self.goal_latitude[-1]+self.goal_half_width[-1],self.z]), 2)
            pygame.draw.line(surface, (225, 230, 255), camera.proj([-self.half_length,self.goal_latitude[-1]-self.goal_half_width[-1],self.z]),
               camera.proj([-self.half_length+20,self.goal_latitude[-1]-self.goal_half_width[-1],self.z]), 2)
            pygame.draw.line(surface, (225, 230, 255), camera.proj([-self.half_length+20,self.goal_latitude[-1]+self.goal_half_width[-1],self.z]),
               camera.proj([-self.half_length+20,self.goal_latitude[-1]-self.goal_half_width[-1],self.z]), 2)


            pygame.draw.line(surface, (245, 180, 165), camera.proj([self.half_length,self.goal_latitude[1]-self.goal_half_width[1],self.z+self.goal_height[1]]),
               camera.proj([self.half_length,self.goal_latitude[1]+self.goal_half_width[1],self.z+self.goal_height[1]]), 5)
            pygame.draw.line(surface, (245, 180, 165), camera.proj([self.half_length,self.goal_latitude[1]-self.goal_half_width[1],self.z]),
               camera.proj([self.half_length,self.goal_latitude[1]-self.goal_half_width[1],self.z+self.goal_height[1]]), 5)
            pygame.draw.line(surface, (245, 180, 165), camera.proj([self.half_length,self.goal_latitude[1]+self.goal_half_width[1],self.z]),
               camera.proj([self.half_length,self.goal_latitude[1]+self.goal_half_width[1],self.z+self.goal_height[1]]), 5)

            pygame.draw.line(surface, (225, 230, 255), camera.proj([self.half_length,self.goal_latitude[1]+self.goal_half_width[1],self.z]),
               camera.proj([self.half_length-20,self.goal_latitude[1]+self.goal_half_width[1],self.z]), 2)
            pygame.draw.line(surface, (225, 230, 255), camera.proj([self.half_length,self.goal_latitude[1]-self.goal_half_width[1],self.z]),
               camera.proj([self.half_length-20,self.goal_latitude[1]-self.goal_half_width[1],self.z]), 2)
            pygame.draw.line(surface, (225, 230, 255), camera.proj([self.half_length-20,self.goal_latitude[1]+self.goal_half_width[1],self.z]),
               camera.proj([self.half_length-20,self.goal_latitude[1]-self.goal_half_width[1],self.z]), 2)



        #draw front flags
        pos=camera.proj([self.half_length,-self.half_width,self.z+8])
        pos[1]-=12
        pygame.draw.line(surface, (180, 180, 185), camera.proj([self.half_length,-self.half_width,self.z]),pos, 3)
        pos[0]-=1
        surface.blit(self.flag_front_image_east,pos)
        pos=camera.proj([-self.half_length,-self.half_width,self.z+8])
        pos[1]-=12
        pygame.draw.line(surface, (180, 180, 185), camera.proj([-self.half_length,-self.half_width,self.z]),pos, 3)
        pos[0]-=1
        surface.blit(self.flag_front_image_west,pos)


