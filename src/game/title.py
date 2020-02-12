from pyglet.text import Label
'''
Created on Feb 12, 2020

@author: Wyatt Muller

The title text for the menu.
'''

class Title():

    def __init__(self, backgroundX, backgroundY, backgroundW, backgroundH):
        self.text_the = Label("The",
                              font_name='Cracked Johnnie',
                              font_size=32,
                              x=backgroundX + (backgroundW / 2),
                              y=backgroundY + (backgroundH / 2) + 220,
                              color=(0, 0, 0, 255),
                              align='center',
                              anchor_x='center',
                              anchor_y='center')
        self.text_dungeonerator = Label("Dungeonerator",
                              font_name='Cracked Johnnie',
                              font_size=48,
                              x=backgroundX + (backgroundW / 2),
                              y=backgroundY + (backgroundH / 2) + 165,
                              color=(50, 50, 50, 255),
                              align='center',
                              anchor_x='center',
                              anchor_y='center')
        
    def draw(self):
        self.text_dungeonerator.draw()
        self.text_the.draw()