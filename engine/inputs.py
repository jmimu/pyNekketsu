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

import pygame,sys

from pygame.locals import *

#Real or fake inputs, for CPU and player
#To handle key up, keydown and joystick

class Inputs():
    player1_R=False
    player1_L=False
    player1_U=False
    player1_D=False
    player1_A=False
    player1_B=False
    player1_C=False
    player1_Esc=False
    player1_Start=False
    player2_R=False
    player2_L=False
    player2_U=False
    player2_D=False
    player2_A=False
    player2_B=False
    player2_C=False
    player2_Esc=False
    player2_Start=False
 
    player1_just_R=False
    player1_just_L=False
    player1_just_U=False
    player1_just_D=False
    player1_just_A=False
    player1_just_B=False
    player1_just_C=False
    player1_just_Esc=False
    player1_just_Start=False
    player2_just_R=False
    player2_just_L=False
    player2_just_U=False
    player2_just_D=False
    player2_just_A=False
    player2_just_B=False
    player2_just_C=False
    player2_just_Esc=False
    player2_just_Start=False
    
    def __init__(self, num_player=0):#num_player: to handle key configs (0=CPU)
        self.num_player=num_player
        self.R=False
        self.L=False
        self.U=False
        self.D=False
        self.A=False
        self.B=False
        self.C=False
        self.Esc=False
        self.Start=False


    @classmethod
    #search for the point, or create it
    def readkeys(cls):
        cls.player1_just_R=False
        cls.player1_just_L=False
        cls.player1_just_U=False
        cls.player1_just_D=False
        cls.player1_just_A=False
        cls.player1_just_B=False
        cls.player1_just_C=False
        cls.player1_just_Esc=False
        cls.player1_just_Start=False
        cls.player2_just_R=False
        cls.player2_just_L=False
        cls.player2_just_U=False
        cls.player2_just_D=False
        cls.player2_just_A=False
        cls.player2_just_B=False
        cls.player2_just_C=False
        cls.player2_just_Esc=False
        cls.player2_just_Start=False
        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
		    if (not cls.player1_Esc):
                        cls.player1_just_Esc=True
                    cls.player1_Esc = True
                if event.key == K_LEFT:
		    if (not cls.player1_L):
                        cls.player1_just_L=True
                    cls.player1_L = True
                if event.key == K_RIGHT:
		    if (not cls.player1_R):
                        cls.player1_just_R=True
                    cls.player1_R = True
                if event.key == K_UP:
		    if (not cls.player1_U):
                        cls.player1_just_U=True
                    cls.player1_U = True
                if event.key == K_DOWN:
		    if (not cls.player1_D):
                        cls.player1_just_D=True
                    cls.player1_D = True
                if event.key == ord('k'):
		    if (not cls.player1_B):
                        cls.player1_just_B=True
                    cls.player1_B = True
                if event.key == ord('l'):
		    if (not cls.player1_A):
                        cls.player1_just_A=True
                    cls.player1_A = True
                if event.key == ord('m'):
		    if (not cls.player1_C):
                        cls.player1_just_C=True
                    cls.player1_C = True
                if event.key == ord('p'):
		    if (not cls.player1_Start):
                        cls.player1_just_Start=True
                    cls.player1_Start = True
                if event.key == K_ESCAPE:
		    if (not cls.player2_Esc):
                        cls.player2_just_Esc=True
                    cls.player2_Esc = True
                if event.key == ord('f'):
		    if (not cls.player2_L):
                        cls.player2_just_L=True
                    cls.player2_L = True
                if event.key == ord('h'):
		    if (not cls.player2_R):
                        cls.player2_just_R=True
                    cls.player2_R = True
                if event.key == ord('t'):
		    if (not cls.player2_U):
                        cls.player2_just_U=True
                    cls.player2_U = True
                if event.key == ord('g'):
		    if (not cls.player2_D):
                        cls.player2_just_D=True
                    cls.player2_D = True
                if event.key == ord('a'):
		    if (not cls.player2_B):
                        cls.player2_just_B=True
                    cls.player2_B = True
                if event.key == ord('z'):
		    if (not cls.player2_A):
                        cls.player2_just_A=True
                    cls.player2_A = True
                if event.key == ord('e'):
		    if (not cls.player2_C):
                        cls.player2_just_C=True
                    cls.player2_C = True
                if event.key == ord('r'):
		    if (not cls.player2_Start):
                        cls.player2_just_Start=True
                    cls.player2_Start = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    cls.player1_Esc = False
                if event.key == K_LEFT:
                    cls.player1_L = False
                if event.key == K_RIGHT:
                    cls.player1_R = False
                if event.key == K_UP:
                    cls.player1_U = False
                if event.key == K_DOWN:
                    cls.player1_D = False
                if event.key == ord('k'):
                    cls.player1_B = False
                if event.key == ord('l'):
                    cls.player1_A = False
                if event.key == ord('m'):
                    cls.player1_C = False
                if event.key == ord('p'):
                    cls.player1_Start = False
                if event.key == K_ESCAPE:
                    cls.player2_Esc = False
                if event.key == ord('f'):
                    cls.player2_L = False
                if event.key == ord('h'):
                    cls.player2_R = False
                if event.key == ord('t'):
                    cls.player2_U = False
                if event.key == ord('g'):
                    cls.player2_D = False
                if event.key == ord('a'):
                    cls.player2_B = False
                if event.key == ord('z'):
                    cls.player2_A = False
                if event.key == ord('e'):
                    cls.player2_C = False
                if event.key == ord('r'):
                    cls.player2_Start = False


    def update(self):#read corresponding key for human player, of just release keys for CPU
        if (self.num_player==1):#it won't work this way... have to hanlde all events at the same time, instead they are lost (won't work with 2 players)
            self.R=Inputs.player1_R
            self.L=Inputs.player1_L
            self.U=Inputs.player1_U
            self.D=Inputs.player1_D
            self.A=Inputs.player1_A
            self.B=Inputs.player1_B
            self.C=Inputs.player1_C
            self.Esc=Inputs.player1_Esc
            self.Start=Inputs.player1_Start
        if (self.num_player==2):#it won't work this way... have to hanlde all events at the same time, instead they are lost (won't work with 2 players)
            self.R=Inputs.player2_R
            self.L=Inputs.player2_L
            self.U=Inputs.player2_U
            self.D=Inputs.player2_D
            self.A=Inputs.player2_A
            self.B=Inputs.player2_B
            self.C=Inputs.player2_C
            self.Esc=Inputs.player2_Esc
            self.Start=Inputs.player2_Start
                    
        if (self.num_player==0):#CPU: the inputs are trigged in PlayerCPU code
            self.R=False
            self.L=False
            self.U=False
            self.D=False
            self.A=False
            self.B=False
            self.C=False
            self.Esc=False
            self.Start=False
                    

