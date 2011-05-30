#! /usr/bin/python

import pygame,sys

from pygame.locals import *

#to draw everything in field world, with a projection

class Camera():
    def __init__(self):
        self.x=0#camera position
        self.y=0
        self.z=0
        self.sx=1#camera scales
        self.sy=1
        self.l=120 #center of the screen
        self.c=128 #center of the screen
    def proj(self,ground_pos,sprite_w=0,sprite_h=0):#ground_pos is a vector in 3d
        px=ground_pos[0]-self.x
        py=ground_pos[1]-self.y
        pz=ground_pos[2]-self.z
        pc=(px*(200.0-py)/200)*self.sx+self.c  -sprite_w/2 #column
        pl=-(py/4+pz)*self.sy+self.l  -sprite_h/2 #line
        screen_pos=[pc,pl]
        return screen_pos

