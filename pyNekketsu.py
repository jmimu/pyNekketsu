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

from retrogamelib import display
from retrogamelib import font
from retrogamelib.constants import *

from retrogamelib import dialog

display.init(scale=2.0, caption="pyNekketsu", res=NESRES)



# set up pygame
#pygame.init()
mainClock = pygame.time.Clock()
nesfont = font.Font(NES_FONT, (255, 255, 255))

# Get the surface from the NES game library
screen = display.get_surface()

difficulty=5

#ask for options
dialogbox = dialog.DialogBox((240, 51), (0, 0, 0),(255, 255, 255), nesfont)
dialogbox.set_dialog([
	"Welcome to pyNekketsu! Press L to go to the next page.", 
	"Select difficulty and press L to start game!"])
menu = dialog.Menu(nesfont, ["too easy", "easy","medium", "hard", "too hard"])

menu_finished=False
title_image=pygame.image.load("data/title.png")
while not menu_finished:
    mainClock.tick(30)
    
    Inputs.readkeys()#read all the actual keys
      
    if (Inputs.player1_Esc or Inputs.player2_Esc):
        pygame.quit()
        sys.exit()

    # If displaying dialog, do events for dialog!
    if not dialogbox.over():
        if Inputs.player1_just_A:
            dialogbox.progress()
    
    # Otherwise, play the "game"
    else:
        
        # Move the menu cursor if you press up or down    
        if Inputs.player1_just_U:
            menu.move_cursor(-1)
        if Inputs.player1_just_D:
            menu.move_cursor(1)
        
        # If you press start, check which option you're on!
        if Inputs.player1_just_A:
            option, text = menu.get_option()
            difficulty=2+option*2
	    menu_finished=True
        
    # Get the surface from the NES game library
    screen = display.get_surface()
    screen.blit(title_image,(0,0))
    
    # Draw the dialog and menu boxes
    if not dialogbox.over():
        dialogbox.draw(screen, (8, 128))
    else:
        menu.draw(screen, (96, 128), background=(0, 0, 0), border=(255, 255, 255))

    # Update and draw the display
    display.update()


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

    
