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
from inputs import Inputs

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

dz=DisplayZoom(3,"pyNekketsu",256, 240)
match=Match(0,2,0,2,5)

while 1:
    if (Inputs.player1_Esc or Inputs.player2_Esc):#pb: what to do if no player1 in game ?
        pygame.quit()
        sys.exit()

    match.update()

    match.draw(dz.surface)
    dz.update()
    mainClock.tick(40)
    
