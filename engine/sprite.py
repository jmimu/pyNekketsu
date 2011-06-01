#! /usr/bin/python


import pygame
import os

#general drawable 2d object (used to compute drawing order)
class Sprite(object):
    #shadow image is static
    shadow_image=pygame.image.load("data/shadow2.png")
    def __init__(self):
        self.image=0
        self.pos = [0, 0, 0]
        
    def draw(self,surface,camera,is_shadow=True):
        if (is_shadow):
            surface.blit(Sprite.shadow_image, camera.proj([self.pos[0],self.pos[1],0],Sprite.shadow_image.get_width(),Sprite.shadow_image.get_height()))
            surface.blit(self.image, camera.proj(self.pos,self.image.get_width(),self.image.get_height()+3))
        else:
            surface.blit(self.image, camera.proj(self.pos,self.image.get_width(),self.image.get_height()+3))



