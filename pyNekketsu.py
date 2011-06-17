#! /usr/bin/python
# -*- coding: utf-8 -*-

#    pyNekketsu
#    Copyright (C) 2011  JM Muller
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import os


import sys
sys.path.insert(0, "engine")

from displayzoom import DisplayZoom
from match import Match
from menu import call_menu
from inputs import Inputs

from retrogamelib import display
from retrogamelib import font
from retrogamelib.constants import *


display.init(scale=2.0, caption="pyNekketsu", res=NESRES)



# set up pygame
#pygame.init()
mainClock = pygame.time.Clock()
nesfont = font.Font(NES_FONT, (255, 255, 255))

# Get the surface from the NES game library
screen = display.get_surface()

difficulty=5

difficulty=call_menu(display,nesfont,mainClock)


#dz=DisplayZoom(2,"pyNekketsu",256, 240)
match=Match(1,1,0,1,difficulty)


while 1:
    screen = display.get_surface()


    if (Inputs.player1_Esc or Inputs.player2_Esc):
        pygame.quit()
        sys.exit()

    match.update()

    match.draw(screen)

    ren = nesfont.render("Score: "+str(match.teamA.nb_goals)+" - "+str(match.teamB.nb_goals))
    screen.blit(ren, (8, 8))

    display.update()
    mainClock.tick(30)

    
