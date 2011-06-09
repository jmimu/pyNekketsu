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
    player2_R=False
    player2_L=False
    player2_U=False
    player2_D=False
    player2_A=False
    player2_B=False
    player2_C=False
    player2_Esc=False
    
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
    
    @classmethod
    #search for the point, or create it
    def readkeys(cls):
        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    cls.player1_Esc = True
                if event.key == K_LEFT:
                    cls.player1_L = True
                if event.key == K_RIGHT:
                    cls.player1_R = True
                if event.key == K_UP:
                    cls.player1_U = True
                if event.key == K_DOWN:
                    cls.player1_D = True
                if event.key == ord('k'):
                    cls.player1_B = True
                if event.key == ord('l'):
                    cls.player1_A = True
                if event.key == ord('m'):
                    cls.player1_C = True
                if event.key == K_ESCAPE:
                    cls.player2_Esc = True
                if event.key == ord('f'):
                    cls.player2_L = True
                if event.key == ord('h'):
                    cls.player2_R = True
                if event.key == ord('t'):
                    cls.player2_U = True
                if event.key == ord('g'):
                    cls.player2_D = True
                if event.key == ord('a'):
                    cls.player2_B = True
                if event.key == ord('z'):
                    cls.player2_A = True
                if event.key == ord('e'):
                    cls.player2_C = True
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
        if (self.num_player==2):#it won't work this way... have to hanlde all events at the same time, instead they are lost (won't work with 2 players)
            self.R=Inputs.player2_R
            self.L=Inputs.player2_L
            self.U=Inputs.player2_U
            self.D=Inputs.player2_D
            self.A=Inputs.player2_A
            self.B=Inputs.player2_B
            self.C=Inputs.player2_C
            self.Esc=Inputs.player2_Esc
                    
        if (self.num_player==0):#CPU: the inputs are trigged in PlayerCPU code
            self.R=False
            self.L=False
            self.U=False
            self.D=False
            self.A=False
            self.B=False
            self.C=False
            self.Esc=False
                    

