from pyglet.text import Label
'''
Created on Feb 11, 2020

@author: Wyatt Muller

Contains the list of buttons on the menu.
'''

class Buttons():
    
    list = []
    
    current_idx = 0

    def __init__(self, game_scale, backgroundX, backgroundY, backgroundW, backgroundH):
        new_button = Button(a_scale=game_scale, name="New Game", xCoord=(backgroundX + (backgroundW / 2)), yCoord=(backgroundY + (backgroundH / 2)))
        new_button.select()
        load_button = Button(a_scale=game_scale, name="Load Game", xCoord=new_button.x, yCoord=new_button.y - (55 * game_scale))
        quit_button = Button(a_scale=game_scale, name="Quit", xCoord=load_button.x, yCoord=load_button.y - (55 * game_scale))
        Buttons.list.append(new_button)
        Buttons.list.append(load_button)
        Buttons.list.append(quit_button)
        
    def next(self):
        Buttons.list[Buttons.current_idx].deselect()
        if (Buttons.current_idx == len(Buttons.list) - 1):
            Buttons.current_idx = 0
        else:
            Buttons.current_idx = Buttons.current_idx + 1
        Buttons.list[Buttons.current_idx].select()
        
    def previous(self):
        Buttons.list[Buttons.current_idx].deselect()
        if (Buttons.current_idx == 0):
            Buttons.current_idx = len(Buttons.list) - 1
        else:
            Buttons.current_idx = Buttons.current_idx - 1
        Buttons.list[Buttons.current_idx].select()
        
    def draw(self):
        for button in Buttons.list:
            button.draw()

class Button(Label):
    
    def __init__(self, a_scale, name, xCoord, yCoord):
        super().__init__(name,
                         font_name='Times New Roman',
                         font_size=32 * a_scale,
                         x=xCoord,
                         y=yCoord,
                         color=(0, 0, 0, 255),
                         align='center',
                         anchor_x='center',
                         anchor_y='center')
        self.button_text = name
        self.game_scale = a_scale
        
    def select(self):
        self.font_size = 48 * self.game_scale
        self.color = (50, 50, 50, 255)
        
    def deselect(self):
        self.font_size = 32 * self.game_scale
        self.color = (0, 0, 0, 255)
        