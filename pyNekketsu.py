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



import pygame, sys, time, random
from pygame.locals import *
from retrogamelib import display
from retrogamelib import font
from retrogamelib.constants import *

display.init(scale=2, caption="pyNekketsu", res=NESRES)

pygame.mixer.pre_init(22050,8,1,1024)


from match import Match
from menu import call_all_menus, show_info, select_teams
from inputs import Inputs




# set up pygame
#pygame.init()
mainClock = pygame.time.Clock()
nesfont = font.Font(NES_FONT, (255, 255, 255))

# Get the surface from the NES game library
screen = display.get_surface()

#show_info(display,nesfont,mainClock)

while 1:
    players_human_teamA,players_human_teamB,difficulty,nb_players_team,match_length=call_all_menus(display,nesfont,mainClock)
    (teamA_filename,teamB_filename)=select_teams(display,nesfont,mainClock)

    match=Match(teamA_filename,teamB_filename)
    match.show_loading(display,nesfont)   
    match.init(players_human_teamA,nb_players_team,players_human_teamB,nb_players_team,difficulty,match_length)
    
    while not match.is_finished:
        screen = display.get_surface()
        
        if (Inputs.player_just_Esc[1] or Inputs.player_just_Esc[2]):
            match.is_finished=True
        
        match.update()
        
        match.draw(screen,nesfont)
        
        display.update()
        mainClock.tick(30)

        
