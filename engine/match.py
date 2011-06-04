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
        self.goal_image=pygame.image.load("data/goal.png")
        self.goaldrawing_time=0
        
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
        
    
    def update(self):
        if (self.goaldrawing_time<10):
            if (self.goaldrawing_time>0):
                self.goaldrawing_time-=1
            for p in self.perso_list:
                p.update(self)

            self.ball.update(self)
            
            if (self.ball.owner==0):
                self.cam.aim_to([self.ball.pos[0],self.ball.pos[1],self.ball.pos[2]/2],0,50)
            else:
                self.cam.aim_to([self.ball.pos[0],self.ball.pos[1],self.ball.pos[2]/2],self.ball.owner.direction,5)
        else:
            self.goaldrawing_time-=1


    def draw(self,surface):
        self.field.draw(surface,self.cam)

        sprite_list=sorted( [self.ball]+self.perso_list,   key=lambda Sprite: -Sprite.pos[1]) #sort all the sprites list with y pos
        for s in sprite_list:
            s.draw(surface,self.cam)
        
        if (self.goaldrawing_time!=0):
            surface.blit(self.goal_image, [0,0])
    



