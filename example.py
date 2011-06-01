#! /usr/bin/python


import pygame
import os


import sys
sys.path.insert(0, "engine")

from perso import Perso
from inputs import Inputs
from displayzoom import DisplayZoom
from camera import Camera
from field import Field
from ball import Ball
from sprite import Sprite

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# Initalise the display
WINDOWWIDTH = 400
WINDOWHEIGHT = 400

dz=DisplayZoom(3,"Yo!",256, 240)
#displayzoom.screen = displayzoom.get_surface()

player = Perso() # Create the player

inputs=Inputs()
cam=Camera()
field=Field()
ball=Ball()

perso_list=[player]
for i in range(10):
    perso_list.append(Perso())


while 1:    
    inputs.update()
    if (inputs.Esc):
        pygame.quit()
        sys.exit()

    for p in perso_list:    
        p.update(inputs,field)

    ball.update()
    
    cam.aim_to(player.pos,player.direction,5)

    field.draw(dz.surface,cam)

    sprite_list=sorted( [ball]+perso_list,   key=lambda Sprite: -Sprite.pos[1])#sort all the sprites list with y pos
    for s in sprite_list:
        s.draw(dz.surface,cam)

    dz.update()
    mainClock.tick(40)
    
