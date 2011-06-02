#! /usr/bin/python


import pygame
import os

from perso import Perso
from perso_cpu import PersoCPU
from perso_player import PersoPlayer
from inputs import Inputs
from camera import Camera
from field import Field
from ball import Ball
from sprite import Sprite



class Match(object):
    def __init__(self):
        self.player1 = PersoPlayer() # Create the player
        self.inputs=Inputs()
        self.cam=Camera()
        self.field=Field()
        self.ball=Ball()
        self.perso_list=[self.player1]
        for i in range(10):
            self.perso_list.append(PersoCPU())
     
    def update(self):
        self.inputs.update()
        if (self.inputs.Esc):
            pygame.quit()
            sys.exit()

        for p in self.perso_list:    
            p.update(self.inputs,self.field)

        self.ball.update(self.field)
        
        self.cam.aim_to(self.player1.pos,self.player1.direction,5)


    def draw(self,surface):
        self.field.draw(surface,self.cam)

        sprite_list=sorted( [self.ball]+self.perso_list,   key=lambda Sprite: -Sprite.pos[1]) #sort all the sprites list with y pos
        for s in sprite_list:
            s.draw(surface,self.cam)



