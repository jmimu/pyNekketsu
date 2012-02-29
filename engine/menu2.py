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
import fnmatch
from math import cos
from xml.dom import minidom

from inputs import Inputs
#from team import Team
from settings import configuration

from retrogamelib import display
from retrogamelib import font
from retrogamelib.constants import *
from retrogamelib import dialog


#read menus.xml file

#Menu : pb : can't mix submenus and settings, and needs an "setting" to exit menu.


class Menu(object):
    all_menus={} #where all menus are copied, to allow referencing and avoid copy

    @classmethod
    def get_menu_by_id(cls,id):
        if (id in cls.all_menus.keys()):
            return cls.all_menus[id]
        else:
            return Menu(id)
    
    @classmethod
    def get_menu_by_xmlnode(cls,xml_node):
        id=xml_node.getElementsByTagName('id')[0].childNodes[0].data
        if (id in cls.all_menus.keys()):
            menu=cls.all_menus[id]
        else:
            menu=Menu(id)
        menu.read_xml(xml_node)
        return menu
        
    def __init__(self,id):
        #print("Add node ",id)
        Menu.all_menus[id]=self
        self.id=0
        self.text=""
        self.choices_submenus=[]#if submenus
        self.choices_submenus_text=[]
        self.choices_variable="" #if has to change a setting
        self.choices_values_value=[]
        self.choices_values_text=[]
        self.choices_values_goto=[] #submenu to go to when value selected (parent if no given)
        self.default_num=0
        self.parent=0
        self.exits=False #if menu is finished after that (only for configs)
        self.dialogtext="" #if there are special instructions
    def read_xml(self,xml_node):
        self.id=xml_node.getElementsByTagName('id')[0].childNodes[0].data
        self.text=xml_node.getElementsByTagName('text')[0].childNodes[0].data
        self.exits=len(xml_node.getElementsByTagName('exits'))>0
        if (len(xml_node.getElementsByTagName('dialogtext'))>0):
            self.dialogtext=xml_node.getElementsByTagName('dialogtext')[0].childNodes[0].data
        #if submenus
        all_choices_node=xml_node.getElementsByTagName('sub-menu')
        for submenu_node in all_choices_node:
            subid=submenu_node.getElementsByTagName('goto')[0].childNodes[0].data
            self.choices_submenus.append(self.get_menu_by_id(subid))
            #change partent of submenu
            self.choices_submenus[-1].parent=self
            self.choices_submenus_text.append(submenu_node.getElementsByTagName('text')[0].childNodes[0].data)
            if (len(submenu_node.getElementsByTagName('default'))>0):
                self.default_num=len(self.choices_submenus)-1
        #if values
        if (len(xml_node.getElementsByTagName('variable'))>0):
            self.variable=xml_node.getElementsByTagName('variable')[0].childNodes[0].data
            if not(self.variable in configuration.keys()):
                configuration[self.variable]="" #define the entry, to avoid bug if no default defined
            all_settings_node=xml_node.getElementsByTagName('setting')
            for setting_node in all_settings_node:
                subtext=setting_node.getElementsByTagName('text')[0].childNodes[0].data
                self.choices_values_text.append(subtext)
                subvalue=setting_node.getElementsByTagName('value')[0].childNodes[0].data
                self.choices_values_value.append(subvalue)
                if (len(setting_node.getElementsByTagName('goto'))>0):
                    self.choices_values_goto.append(self.get_menu_by_id(setting_node.getElementsByTagName('goto')[0].childNodes[0].data))
                    #change partent of submenu
                    self.choices_values_goto[-1].parent=self
                else:
                    self.choices_values_goto.append(0)
                if (len(setting_node.getElementsByTagName('default'))>0):
                    self.default_num=len(self.choices_values_text)-1
                    #set this value to "configuration"
                    configuration[self.variable]=subvalue
    def display(self,display,font,mainClock):
        title_image=pygame.image.load("data/title.png")
        dlg=0
        selected_option=self.default_num
        if (len(self.choices_values_value)>0):#if settings, read in "configuration"
            selected_option=0
            for val in self.choices_values_value :
                if (val==configuration[self.variable]):
                    break
                selected_option+=1
            if (selected_option==len(self.choices_values_value)):
                selected_option=self.default_num
            dlg = dialog.Menu(font, self.choices_values_text)
        else:#look for submenus
            dlg = dialog.Menu(font, self.choices_submenus_text)
        
        dlg.option=selected_option
        if (len(self.dialogtext)>0):
            dialogbox = dialog.DialogBox((240, 51), (0, 0, 0),(255, 255, 255), font)
            dialogbox.set_dialog([self.dialogtext])
        while 1:
            mainClock.tick(30)
            Inputs.readkeys()#read all the actual keys
            if (Inputs.player_just_Esc[1] or Inputs.player_just_Esc[2]):
                pygame.quit()
                sys.exit()
            # Move the menu cursor if you press up or down    
            if Inputs.player_just_U[1]:
                dlg.move_cursor(-1)
            if Inputs.player_just_D[1]:
                dlg.move_cursor(1)
            # If you press A, check which option you're on!
            if Inputs.player_just_A[1]:
                if (len(self.choices_values_value)>0):#if settings
                    configuration[self.variable]=self.choices_values_value[dlg.get_option()[0]]
                    if (self.choices_values_goto[dlg.get_option()[0]]!=0):
                        self.choices_values_goto[dlg.get_option()[0]].display(display,font,mainClock)
                    else:
                        if (self.exits):
                            configuration["exit_menu"]="yes"
                        return
                    
                else:#if submenus
                    #print(dlg.get_option())
                    self.choices_submenus[dlg.get_option()[0]].display(display,font,mainClock)
            ## If you press B, cancel 
            if Inputs.player_just_B[1]:
                if (self.id!="menu_welcome"):
                    Inputs.player_just_B[1]=False
                    return
                else:
                    print("Nothing to do...")
            
            #if returns from a sub-menu asking to exit :
            if (configuration["exit_menu"]=="yes"):
                return
            
            # Get the surface from the NES game library
            screen = display.get_surface()
            screen.blit(title_image,(0,0))
            
            # Draw the menu boxes
            ren = font.render(self.text)
            screen.blit(ren, (8, 112))
            dlg.draw(screen, (16, 128), background=(0, 0, 0), border=(255, 255, 255))
            if (len(self.dialogtext)>0):
                dialogbox.draw(screen, (8, 180))
            # Update and draw the display
            display.update()





#open xml file
xmldoc = minidom.parse("data/menus.xml")
menus_node = xmldoc.getElementsByTagName('menus')[0]
all_menus_node=menus_node.getElementsByTagName('menu')
for menu_node in all_menus_node:
    Menu.get_menu_by_xmlnode(menu_node)

#then read "config.txt" file, to have default settings
config_file = open("config.txt","r")
line = config_file.readline()
while line:
    if (line[0]=="#"):
        variable=line[1:-1].split()[0]
        value=config_file.readline()
        value=value.split()[0]
        configuration[variable]=value
        print("conf["+variable+"]="+value+".")
    line = config_file.readline()

config_file.close()


#print("Welcome:")
#menu_depart=Menu.all_menus["menu_welcome"]
#if (menu_depart.parent!=0):
#    print("Parent: ",menu_depart.parent.id)
#for i in range(0,len(menu_depart.choices_submenus)):
#    if (i==menu_depart.default_num):
#        print "**"
#    print("- ",menu_depart.choices_submenus_text[i])
#
#print("Options:")
#menu_opt=menu_depart.choices_submenus[2]
#if (menu_opt.parent!=0):
#    print("Parent: ",menu_opt.parent.id)
#for i in range(0,len(menu_opt.choices_submenus)):
#    if (i==menu_opt.default_num):
#        print "**"
#    print("- ",menu_opt.choices_submenus_text[i])
#    
#
#print("Sound:")
#menu_snd=menu_opt.choices_submenus[0]
#if (menu_snd.parent!=0):
#    print("Parent: ",menu_snd.parent.id)
#for i in range(0,len(menu_snd.choices_submenus)):
#    if (i==menu_snd.default_num):
#        print "**"
#    print("- ",menu_snd.choices_submenus_text[i])
#for i in range(0,len(menu_snd.choices_values_text)):
#    if (i==menu_snd.default_num):
#        print "**"
#    print("+ ",menu_snd.choices_values_text[i])
#    
#
#print(configuration)


