#! /usr/bin/python


import pygame
import os
import random
from perso import Perso
from inputs import Inputs

class PersoPlayer(Perso):
    
    def __init__(self,team,num_player=1,num_player_image_name="data/1.png"):
        Perso.__init__(self,team)
        self.inputs=Inputs(1) #key config: player 1
        self.num_player=num_player
        self.num_player_image=pygame.image.load(num_player_image_name)
        
    def update(self,match):
        Perso.update(self,match) 
        
    def draw(self,surface,camera,is_shadow=True):
        Perso.draw(self,surface,camera,is_shadow)
        projection=camera.proj([self.pos[0],self.pos[1],self.pos[2]],self.team.image.get_width(),self.team.image.get_height()*0)
        surface.blit(self.num_player_image, camera.proj([self.pos[0],self.pos[1],self.pos[2]],self.team.image.get_width(),self.team.image.get_height()*0))
        has_to_draw_arrow=False
        if (projection[0]>256):
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
        


