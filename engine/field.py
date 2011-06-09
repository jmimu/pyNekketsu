#! /usr/bin/python

import pygame,sys

from pygame.locals import *

#Field represents the soccer field: size, drawing, goal position...

class Field():
    def __init__(self):
        self.half_length=100
        self.half_width=50
        self.z=0.0
        
        self.goal_half_width={}#-1: west goal, +1: east goal
        self.goal_height={}
        self.goal_latitude={}
        
        self.goal_half_width[-1]=20#west goal
        self.goal_height[-1]=15
        self.goal_latitude[-1]=0#where the goal center is inside field width
        self.goal_half_width[1]=20#east goal
        self.goal_height[1]=15
        self.goal_latitude[1]=0#where the goal center is inside field width
        self.bounce_damp=0.6#1=perfect
        self.roll_damp=0.9#1=perfect
    def collide_with_player(self,player): #block a player inside the field
        # If we're at ground level, stop.
        if (player.pos[2] <= self.z):
            player.pos[2] = self.z
            player.jump_speed = 0
            if (player.state=="jump"):
                player.state="walk"
                player.anim_index=0
                player.previous_pos[:]=player.pos[:]
        
        # Keep the player in bounds
        if player.pos[0] < -self.half_length:
            player.pos[0] = -self.half_length
        if player.pos[0] > self.half_length:
            player.pos[0] = self.half_length
        if player.pos[1] < -self.half_width:
            player.pos[1] = -self.half_width
        if player.pos[1] > self.half_width:
            player.pos[1] = self.half_width


    def draw(self,surface,camera):
        #background
        horizon_x,horizon_y=camera.proj([0,200,self.z])
        pygame.draw.rect(surface, ( 200, 200, 255), (0, 0,256,horizon_y))
        pygame.draw.rect(surface, ( 50, 100,   0), (0, horizon_y, 256, 241-horizon_y))
        pygame.draw.rect(surface, (255, 200, 185), (0, horizon_y+2, 256,  1), 1)
        
        #hz lines
        for x in range(11):
            pygame.draw.line(surface, (185, 200, 105), camera.proj([-self.half_length+x*20,-self.half_width,self.z]), camera.proj([-self.half_length+x*20,self.half_width,self.z]), 1)
        for y in range(6):
            pygame.draw.line(surface, (185, 200, 105), camera.proj([-self.half_length,-self.half_width+y*20,self.z]), camera.proj([self.half_length,-self.half_width+y*20,self.z]), 1)
        pygame.draw.line(surface, (225, 230, 255), camera.proj([-self.half_length,-self.half_width,self.z]), camera.proj([-self.half_length,self.half_width,self.z]), 3)
        pygame.draw.line(surface, (225, 230, 255), camera.proj([-self.half_length,self.half_width,self.z]), camera.proj([self.half_length,self.half_width,self.z]), 3)
        pygame.draw.line(surface, (225, 230, 255), camera.proj([self.half_length,self.half_width,self.z]), camera.proj([self.half_length,-self.half_width,self.z]), 3)
        pygame.draw.line(surface, (225, 230, 255), camera.proj([self.half_length,-self.half_width,self.z]), camera.proj([-self.half_length,-self.half_width,self.z]), 3)
        pygame.draw.line(surface, (225, 230, 255), camera.proj([0,self.half_width,self.z]), camera.proj([0,-self.half_width,self.z]), 3)
     
        #goals
        pygame.draw.line(surface, (245, 180, 165), camera.proj([-self.half_length,self.goal_latitude[-1]-self.goal_half_width[-1],self.z+self.goal_height[-1]]),
           camera.proj([-self.half_length,self.goal_latitude[-1]+self.goal_half_width[-1],self.z+self.goal_height[-1]]), 5)
        pygame.draw.line(surface, (245, 180, 165), camera.proj([-self.half_length,self.goal_latitude[-1]-self.goal_half_width[-1],self.z]),
           camera.proj([-self.half_length,self.goal_latitude[-1]-self.goal_half_width[-1],self.z+self.goal_height[-1]]), 5)
        pygame.draw.line(surface, (245, 180, 165), camera.proj([-self.half_length,self.goal_latitude[-1]+self.goal_half_width[-1],self.z]),
           camera.proj([-self.half_length,self.goal_latitude[-1]+self.goal_half_width[-1],self.z+self.goal_height[-1]]), 5)

        pygame.draw.line(surface, (245, 180, 165), camera.proj([self.half_length,self.goal_latitude[1]-self.goal_half_width[1],self.z+self.goal_height[1]]),
           camera.proj([self.half_length,self.goal_latitude[1]+self.goal_half_width[1],self.z+self.goal_height[1]]), 5)
        pygame.draw.line(surface, (245, 180, 165), camera.proj([self.half_length,self.goal_latitude[1]-self.goal_half_width[1],self.z]),
           camera.proj([self.half_length,self.goal_latitude[1]-self.goal_half_width[1],self.z+self.goal_height[1]]), 5)
        pygame.draw.line(surface, (245, 180, 165), camera.proj([self.half_length,self.goal_latitude[1]+self.goal_half_width[1],self.z]),
           camera.proj([self.half_length,self.goal_latitude[1]+self.goal_half_width[1],self.z+self.goal_height[1]]), 5)






