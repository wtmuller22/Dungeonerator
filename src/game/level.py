from pyglet.text import Label
'''
Created on Feb 15, 2020

@author: Wyatt Muller

Displays the current level of the player.
'''

class Level(Label):

    def __init__(self, a_scale, backgroundX, backgroundY):
        super().__init__('Level: 0',
                         font_name='Cracked Johnnie',
                         font_size=16 * a_scale,
                         x=backgroundX + (40 * a_scale),
                         y=backgroundY + (960 * a_scale),
                         color=(140, 0, 0, 255))
        
    def update_level(self, new_level):
        self.text = 'Level: ' + str(new_level)