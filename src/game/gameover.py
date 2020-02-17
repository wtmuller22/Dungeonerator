from pyglet.text import Label
'''
Created on Feb 15, 2020

@author: Wyatt Muller

Displays the Game Over text.
'''

class GameOver(Label):

    def __init__(self, backgroundX, backgroundY):
        super().__init__('Game Over',
                         font_name='Cracked Johnnie',
                         font_size=56,
                         x=backgroundX + 500,
                         y=backgroundY + 500,
                         color=(140, 0, 0, 0),
                         anchor_x='center',
                         anchor_y='center',
                         align='center')
