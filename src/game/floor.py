from pyglet.sprite import Sprite
from pyglet import image
'''
Created on Feb 11, 2020

@author: Wyatt Muller

The background/floor viewed in game.
'''

class Floor(Sprite):
    
    title = image.load('images/TitleScreen.png')
    cave = image.load('images/CaveGround.png')

    def __init__(self, windowW, windowH):
        super().__init__(img=Floor.title)
        self.x = (windowW / 2) - (self.width / 2)
        self.y = (windowH / 2) - (self.height / 2)
        self.curr_img = 0
        
    def switch_image(self):
        if (self.curr_img == 0):
            self.image=Floor.cave
            self.curr_img = 1
        else:
            self.image=Floor.title
            self.curr_img = 0