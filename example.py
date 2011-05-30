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
    pygame.draw.rect(dz.surface, ( 50, 100,   0), (0, 180, 256, 60))
    pygame.draw.rect(dz.surface, (255, 200, 185), (0, 182, 256,  1), 1)
    
    pygame.draw.line(dz.surface, (225, 230, 255), (40,188), (10, 230), 3)
    pygame.draw.line(dz.surface, (225, 230, 255), (10, 230), (246, 230), 3)
    pygame.draw.line(dz.surface, (225, 230, 255), (246, 230), (216, 188), 3)
    pygame.draw.line(dz.surface, (225, 230, 255), (216, 188), (40,188), 3)
    
    
    player_drawn_pos=player.pos[0]-player.pos[1]/20,180-player.pos[2]-player.pos[1]/10
    dz.surface.blit(player.image, player_drawn_pos)
    
    dz.update()
    mainClock.tick(40)
    
