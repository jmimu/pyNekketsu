#! /usr/bin/python


import pygame
import os


import sys
sys.path.insert(0, "engine")

from perso import Player
from inputs import Inputs
from displayzoom import DisplayZoom

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Initalise the display
WINDOWWIDTH = 400
WINDOWHEIGHT = 400

dz=DisplayZoom(4,"Yo!",256,192)
#displayzoom.screen = displayzoom.get_surface()

player = Player() # Create the player

inputs=Inputs()




while 1:    
    inputs.update()
    if (inputs.Esc):
        pygame.quit()
        sys.exit()
    
    player.update(inputs)
    
    dz.surface.fill((200, 200, 255))
    pygame.draw.rect(dz.surface, ( 50, 100,   0), (0, 180, 256, 32))
    pygame.draw.rect(dz.surface, (255, 200, 185), (0, 182, 256,  1), 1)
    dz.surface.blit(player.image, player.pos)
    
    dz.update()
    mainClock.tick(40)
    
