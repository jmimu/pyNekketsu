#! /usr/bin/python


import pygame
import os


class Player(object):
    
    def __init__(self):
        self.image = pygame.image.load("data/walk_A.png")
        self.pos = [32, 112]
        self.jump_speed = 0
    
    def update(self,inputs):
        # Move if LEFT or RIGHT is being pressed.
        if inputs.L:
            self.pos[0] -= 3
        if inputs.R:
            self.pos[0] += 3
        
        
        # Jump if the player taps the A button
        if inputs.A:
            self.jump_speed = -5
            
        # Update the player
        
        # Increase the y position by the jump speed
        self.pos[1] += self.jump_speed
        self.jump_speed += 0.4
        
        # If we're at ground level, stop.
        if self.pos[1] > 160:
            self.pos[1] = 160
            self.jump_speed = 0
        
        # Keep the player in-bounds
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[0] > 240:
            self.pos[0] = 240


