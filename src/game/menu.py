from game.buttons import Buttons
from game.title import Title
'''
Created on Feb 12, 2020

@author: Wyatt Muller

The menu for the game.
'''

class Menu():

    def __init__(self, a_scale, backgroundX, backgroundY, backgroundW, backgroundH):
        self.title_text = Title(game_scale=a_scale, backgroundX=backgroundX, backgroundY=backgroundY, backgroundW=backgroundW, backgroundH=backgroundH)
        self.menu_buttons = Buttons(game_scale=a_scale, backgroundX=backgroundX, backgroundY=backgroundY, backgroundW=backgroundW, backgroundH=backgroundH)
        
    def draw(self):
        self.title_text.draw()
        self.menu_buttons.draw()
        
    def get_current_idx(self) -> int:
        return self.menu_buttons.current_idx
    
    def next(self):
        self.menu_buttons.next()
        
    def previous(self):
        self.menu_buttons.previous()