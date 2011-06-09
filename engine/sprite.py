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


