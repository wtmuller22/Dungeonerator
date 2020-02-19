from pyglet.sprite import Sprite
from pyglet import image
'''
Created on Feb 18, 2020

@author: Wyatt Muller

The visibility of the player.
'''

class Visibility(Sprite):
    
    darkness = image.load_animation('images/Visibility.gif', None, None)

    def __init__(self):
        super().__init__(img=Visibility.darkness)
        self.scale = 4
        
    def update_coords(self, aX, aY):
        self.x = aX - (self.scale * 600)
        self.y = aY - (self.scale * 600)