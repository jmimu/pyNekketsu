#! /usr/bin/python


import pygame
import os


import sys
sys.path.insert(0, "engine")

from perso import Player
from inputs import Inputs
from displayzoom import DisplayZoom
from camera import Camera

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



while 1:    
    inputs.update()
    if (inputs.Esc):
        pygame.quit()
        sys.exit()
    
    player.update(inputs)
    
    dz.surface.fill((200, 200, 255))
    pygame.draw.rect(dz.surface, ( 50, 100,   0), (0, 80, 256, 160))
    pygame.draw.rect(dz.surface, (255, 200, 185), (0, 82, 256,  1), 1)
    
    
    pygame.draw.line(dz.surface, (225, 230, 255), cam.proj([-100,-50,0]), cam.proj([-100,50,0]), 3)
    pygame.draw.line(dz.surface, (225, 230, 255), cam.proj([-100,50,0]), cam.proj([100,50,0]), 3)
    pygame.draw.line(dz.surface, (225, 230, 255), cam.proj([100,50,0]), cam.proj([100,-50,0]), 3)
    pygame.draw.line(dz.surface, (225, 230, 255), cam.proj([100,-50,0]), cam.proj([-100,-50,0]), 3)
    dz.surface.blit(player.image, cam.proj(player.pos,player.image.get_width(),player.image.get_height()))
    
    dz.update()
    mainClock.tick(40)
    
