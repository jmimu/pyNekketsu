#! /usr/bin/python


import pygame
import os


import sys
sys.path.insert(0, "engine")

from displayzoom import DisplayZoom
from match import Match
from inputs import Inputs

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

dz=DisplayZoom(3,"pyNekketsu",256, 240)
match=Match()

while 1:
    if (Inputs.player1_Esc or Inputs.player2_Esc):#pb: what to do if no player1 in game ?
        pygame.quit()
        sys.exit()

    match.update()

    match.draw(dz.surface)
    dz.update()
    mainClock.tick(40)
    
