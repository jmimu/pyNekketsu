#! /usr/bin/python


import pygame
import os


import sys
sys.path.insert(0, "engine")

from perso import Player
from inputs import Inputs
from displayzoom import DisplayZoom
from camera import Camera
from field import Field
from ball import Ball

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Initalise the display
WINDOWWIDTH = 400
WINDOWHEIGHT = 400

dz=DisplayZoom(3,"Yo!",256, 240)
#displayzoom.screen = displayzoom.get_surface()

player = Player() # Create the player

inputs=Inputs()
cam=Camera()
field=Field()
ball=Ball()


while 1:    
    inputs.update()
    if (inputs.Esc):
        pygame.quit()
        sys.exit()
    
    player.update(inputs,field)
    ball.update(inputs)
    
    cam.aim_to(player.pos,player.direction,5)

    field.draw(dz.surface,cam)

    player.draw(dz.surface,cam)
    ball.draw(dz.surface,cam)
    #dz.surface.blit(shadow_image, cam.proj([player.pos[0],player.pos[1],0],shadow_image.get_width(),shadow_image.get_height()))
    #dz.surface.blit(player.image, cam.proj(player.pos,player.image.get_width(),player.image.get_height()+3))
    
    #dz.surface.blit(shadow_image, cam.proj([ball.pos[0],ball.pos[1],0],shadow_image.get_width(),shadow_image.get_height()))   
    #dz.surface.blit(ball.image, cam.proj(ball.pos,ball.image.get_width(),ball.image.get_height()+3))
    
    dz.update()
    mainClock.tick(40)
    
