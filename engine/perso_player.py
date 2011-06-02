#! /usr/bin/python


import pygame
import os
import random
from perso import Perso

class PersoPlayer(Perso):
    
    def __init__(self):
        Perso.__init__(self)
        
    def update(self,inputs,field):
        if inputs.L:
            self.pos[0] -= 1
            self.direction = -1
        if inputs.R:
            self.pos[0] += 1
            self.direction = +1
        if inputs.U:
            self.pos[1] += 1
        if inputs.D:
            self.pos[1] -= 1
        if (inputs.L or inputs.R or inputs.U or inputs.D):
            if (self.state=="walk"):
                self.anim_index += 0.2
        
        if (self.anim_index>=len(self.anim[self.direction][self.state])):
            self.anim_index=0
        self.image = self.anim[self.direction][self.state][int(self.anim_index)]
        
        # Jump if the player taps the A button
        if (inputs.A and self.pos[2] == 0):
            self.jump_speed = 2.5
            self.state="jump"
            self.anim_index=0
            
        Perso.update(self,inputs,field) 
