#! /usr/bin/python


import pygame
import os
import random
from perso import Perso
from inputs import Inputs

class PersoCPU(Perso):
    
    def __init__(self):
        Perso.__init__(self)
        self.inputs=Inputs(0)
        
    def update(self,match):
        Perso.update(self,match) 
        self.think(match)

    def think(self,match):#press on virtual keys
        self.inputs.B=True
