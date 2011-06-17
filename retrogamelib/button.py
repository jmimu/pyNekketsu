import pygame
import os

from constants import *

class Handler(object):
    
    def __init__(self):
        """Init the input object
        """
        
        pygame.joystick.init()
        self.bound = {}
        self.pressed = {}
        self.held = {"key": [], "joy": [], "dpad": []}
        
        self.bind_key(A_BUTTON, pygame.K_z)
        self.bind_key(A_BUTTON, 2)
        self.bind_key(B_BUTTON, pygame.K_x)
        self.bind_key(B_BUTTON, 1)
        self.bind_key(START, pygame.K_RETURN)
        self.bind_key(START, 8)
        self.bind_key(SELECT, pygame.K_RSHIFT)
        self.bind_key(SELECT, 9)
     
        self.bind_key(LEFT, pygame.K_LEFT)
        self.bind_key(LEFT, "dleft")
        self.bind_key(RIGHT, pygame.K_RIGHT)
        self.bind_key(RIGHT, "dright")
        self.bind_key(UP, pygame.K_UP)
        self.bind_key(UP, "dup")
        self.bind_key(DOWN, pygame.K_DOWN)
        self.bind_key(DOWN, "ddown")
        
        self.joystick = None
        for i in range(pygame.joystick.get_count()):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()
    
    def handle_input(self):
        """Check for new button presses -> return None
        """
        
        self.events = pygame.event.get()
        self.pressed = {"key": [], "joy": [], "dpad": []}
        self.released = {"key": [], "joy": [], "dpad": []}
        for e in self.events:
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                self.pressed["key"].append(e.key)
                self.held["key"].append(e.key)
            if e.type == pygame.KEYUP:
                if e.key in self.held["key"]:
                    self.held["key"].remove(e.key)
                    self.released["key"].append(e.key)
            if e.type == pygame.JOYBUTTONDOWN:
                self.pressed["joy"].append(e.button)
                self.held["joy"].append(e.button)
            if e.type == pygame.JOYBUTTONUP:
                if e.button in self.held["joy"]:
                    self.held["joy"].remove(e.button)
                    self.released["joy"].append(e.button)
            if e.type == pygame.JOYHATMOTION:
                vals = []
                if e.value[0]<0:
                    vals.append("dleft")
                if e.value[0]>0:
                    vals.append("dright")
                if e.value[1]>0:
                    vals.append("dup")
                if e.value[1]<0:
                    vals.append("ddown")
                for b in ["dleft", "dright", "dup", "ddown"]:
                    if b in self.held["dpad"]:
                        self.held["dpad"].remove(b)
                        self.released["dpad"].append(b)
                else:
                    for v in vals:
                        self.pressed["dpad"].append(v)
                        self.held["dpad"].append(v)
    
    def bind_key(self, value, key):
        """Bind a value to a key -> return None
        """
        
        if not value in self.bound.iterkeys():
            self.bound[value] = []
        self.bound[value].append(key)

    def is_pressed(self, value):
        """Check if a button was just pressed. -> return bool
        """
        
        if value in self.bound.iterkeys():
            bound = self.bound[value]
        
        for key in self.pressed.iterkeys():
            for i in self.pressed[key]:
                if i in bound:
                    return True
        return False

    def is_held(self, value):
        """Check if a button is being held. -> return bool
        """
        
        if value in self.bound.iterkeys():
            bound = self.bound[value]
        
        for key in self.held.iterkeys():
            for i in self.held[key]:
                if i in bound:
                    return True
        return False

    def is_released(self, value):
        """Check if a button is being released. -> return bool
        """
        
        if value in self.bound.iterkeys():
            bound = self.bound[value]
        
        for key in self.held.iterkeys():
            for i in self.released[key]:
                if i in bound:
                    return True
        return False

handler = Handler()
handle_input = handler.handle_input
is_pressed = handler.is_pressed
is_released = handler.is_released
is_held = handler.is_held

def test():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.display.set_mode((320, 240))
    
    while 1:
        pygame.time.wait(15)
        handle_input()
        if is_held(A_BUTTON):
            print "You're holding the A button!"
        if is_pressed(START):
            print "You pressed Start!"
        if is_pressed(SELECT):
            print "You pressed Select!"  
        if is_pressed(LEFT):
            print "You pressed LEFT!"
        if is_pressed(RIGHT):
            print "You pressed RIGHT!"
        if is_held(LEFT):
            print "You are holding left"
        if is_held(DOWN):
            print "You are holding down"

if __name__ == "__main__":
    test()
