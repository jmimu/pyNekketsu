#! /usr/bin/python


import pygame
import os


import sys
sys.path.insert(0, "engine")

from displayzoom import DisplayZoom
from match import Match

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

dz=DisplayZoom(3,"Yo!",256, 240)
match=Match()

while 1:    
    match.update()

    match.draw(dz.surface)
    dz.update()
    mainClock.tick(40)
    
