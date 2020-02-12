import pyglet
from pyglet import image
'''
Created on Feb 11, 2020

@author: Wyatt Muller

The background/floor viewed in game.
'''

class Floor(pyglet.sprite.Sprite):
    
    title = image.load('images/TitleScreen.png')

    def __init__(self):
        super().__init__(img=Floor.title)
        self.x = 750 - (self.width / 2)
        self.y = 500 - (self.height / 2)
        