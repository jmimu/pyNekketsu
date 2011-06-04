#! /usr/bin/python


import pygame
import os

import sys
from perso import Perso
from perso_cpu import PersoCPU
from perso_player import PersoPlayer
from inputs import Inputs
from camera import Camera
from field import Field
from ball import Ball
from sprite import Sprite
from team import Team


class Match(object):
    def __init__(self):
        self.cam=Camera()
        self.field=Field()
        self.ball=Ball()
        self.perso_list=[]
        self.teamA=Team("data/teamA.png","Les Bogoss",1,1)
        self.player1 = PersoPlayer(self.teamA) # Create the player
        self.teamA.persos.append(self.player1)
        self.perso_list+=self.teamA.persos
        self.teamB=Team("data/teamB.png","Les Klass",-1,2)
        self.perso_list+=self.teamB.persos
        
        for p in self.perso_list:
            print(p)
    
    def update(self):
        for p in self.perso_list:    
            p.update(self)

        self.ball.update(self)
        
        if (self.ball.owner==0):
            self.cam.aim_to(self.ball.pos,0,5)
        else:
            self.cam.aim_to(self.ball.pos,self.ball.owner.direction,5)


    def draw(self,surface):
        self.field.draw(surface,self.cam)

        sprite_list=sorted( [self.ball]+self.perso_list,   key=lambda Sprite: -Sprite.pos[1]) #sort all the sprites list with y pos
        for s in sprite_list:
            s.draw(surface,self.cam)



