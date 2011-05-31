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


while 1:    
    inputs.update()
    if (inputs.Esc):
        pygame.quit()
        sys.exit()
    
    player.update(inputs,field)
    
    cam.aim_to(player.pos,5)

    field.draw(dz.surface,cam)

    dz.surface.blit(player.image, cam.proj(player.pos,player.image.get_width(),player.image.get_height()))
    
    dz.update()
    mainClock.tick(40)
    
