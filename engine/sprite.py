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

#general drawable 2D object (used to compute drawing order)
class Sprite(object):
    #shadow image is static
    shadow_image=pygame.image.load("data/shadow2.png")
    def __init__(self):
        self.image=0
        self.pos = [0, 0, 0]
        self.previous_pos = [0, 0, 0]
        
    def draw(self,surface,camera,is_shadow=True):
        if (is_shadow):
            surface.blit(Sprite.shadow_image, camera.proj([self.pos[0],self.pos[1],0],Sprite.shadow_image.get_width(),Sprite.shadow_image.get_height()-3))
            surface.blit(self.image, camera.proj(self.pos,self.image.get_width(),self.image.get_height()))
        else:
            surface.blit(self.image, camera.proj(self.pos,self.image.get_width(),self.image.get_height()))

#merge head and body pictures
#give colors (R,G,B)
def compileimage(which_team,body_img,which_head,head_img,head_pos,top_color,bottom_color,skin_color):
    body_filename="data/bodies/team"+str(which_team)+"/"+body_img
    body_image=pygame.image.load(body_filename)
    #change top color from (0,255,255) to top_color 
    #change bottom color from (0,128,0) to bottom_color 
    for x in range(body_image.get_width()):
        for y in range(body_image.get_height()):
            if (body_image.get_at((x,y))==(0,255,255)):
                body_image.set_at((x,y),top_color)
            if (body_image.get_at((x,y))==(0,128,0)):
                body_image.set_at((x,y),bottom_color)


    head_filename="data/heads/head"+str(which_head)+"/"+head_img
    head_image=pygame.image.load(head_filename)

    #total_surface=pygame.Surface(body_image.get_rect()[2:4]) #create a surface as big as the body image
    total_surface=body_image.copy() #create a surface as big as the body image
    total_surface.blit(body_image,(0,0))
    total_surface.blit(head_image,head_pos)

    #change skin color from (255,119,99) to skin_color 
    for x in range(total_surface.get_width()):
        for y in range(total_surface.get_height()):
            if (total_surface.get_at((x,y))==(255,119,99)):
                total_surface.set_at((x,y),skin_color)
 
    return total_surface

