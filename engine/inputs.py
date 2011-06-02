#! /usr/bin/python

import pygame,sys

from pygame.locals import *

#To handle key up, keydown and joystick

class Inputs():
    def __init__(self):
        self.R=False
        self.L=False
        self.U=False
        self.D=False
        self.A=False
        self.B=False
        self.C=False
        self.Esc=False
    def update(self):
        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.Esc = True
                if event.key == K_LEFT:
                    self.L = True
                if event.key == K_RIGHT:
                    self.R = True
                if event.key == K_UP:
                    self.U = True
                if event.key == K_DOWN:
                    self.D = True
                if event.key == ord('w'):
                    self.B = True
                if event.key == ord('x'):
                    self.A = True
                if event.key == ord('c'):
                    self.C = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.Esc = False
                if event.key == K_LEFT:
                    self.L = False
                if event.key == K_RIGHT:
                    self.R = False
                if event.key == K_UP:
                    self.U = False
                if event.key == K_DOWN:
                    self.D = False
                if event.key == ord('w'):
                    self.B = False
                if event.key == ord('x'):
                    self.A = False
                if event.key == ord('c'):
                    self.C = False

