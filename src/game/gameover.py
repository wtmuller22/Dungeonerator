from pyglet.text import Label
'''
Created on Feb 15, 2020

@author: Wyatt Muller

Displays the Game Over text.
'''

class GameOver():

    def __init__(self, backgroundX, backgroundY):
        self.game_over = Label('Game Over',
                         font_name='Cracked Johnnie',
                         font_size=56,
                         x=backgroundX + 500,
                         y=backgroundY + 500,
                         color=(140, 0, 0, 0),
                         anchor_x='center',
                         anchor_y='center',
                         align='center')
        self.restart = Label('Press W To Menu',
                         font_name='Times New Roman',
                         font_size=24,
                         x=backgroundX + 500,
                         y=backgroundY + 440,
                         color=(50, 50, 50, 0),
                         anchor_x='center',
                         anchor_y='center',
                         align='center')

    def draw(self):
        self.game_over.draw()
        self.restart.draw()
        
    def make_visible(self):
        self.game_over.color = (140, 0, 0, 255)
        self.restart.color = (50, 50, 50, 255)