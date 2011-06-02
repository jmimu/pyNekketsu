#! /usr/bin/python


import pygame
import os
import random
from perso import Perso

class PersoPlayer(Perso):
    
    def __init__(self):
        Perso.__init__(self)
        
    def update(self,match):
        Perso.update(self,match) 

        if (self.state=="walk"):
            if match.inputs.L:
                self.pos[0] -= 1
                self.direction = -1
            if match.inputs.R:
                self.pos[0] += 1
                self.direction = +1
            if match.inputs.U:
                self.pos[1] += 1
            if match.inputs.D:
                self.pos[1] -= 1
            if (match.inputs.L or match.inputs.R or match.inputs.U or match.inputs.D):
                self.anim_index += 0.2
            # Jump if the player taps the A button
            if (match.inputs.C and self.pos[2] == 0):
                self.jump_speed = 2.5
                self.state="jump"
                self.anim_index=0
                
            if (match.inputs.B):
                if (self.has_ball!=0):
                    self.shoot(match)
            if (match.inputs.A):
                if (self.has_ball==0):
                    self.attack(match)
       




