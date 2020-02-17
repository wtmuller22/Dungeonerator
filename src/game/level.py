from pyglet.text import Label
'''
Created on Feb 15, 2020

@author: Wyatt Muller

Displays the current level of the player.
'''

class Level(Label):

    def __init__(self, backgroundX, backgroundY):
        super().__init__('Level: 0',
                         font_name='Cracked Johnnie',
                         font_size=16,
                         x=backgroundX + 40,
                         y=backgroundY + 960,
                         color=(140, 0, 0, 255))
        
    def update_level(self, new_level):
        self.text = 'Level: ' + str(new_level)