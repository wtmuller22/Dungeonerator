from pyglet.text import Label
'''
Created on Feb 11, 2020

@author: Wyatt Muller

Contains the list of buttons on the menu.
'''

class Buttons():
    
    list = []
    
    current_idx = 0

    def __init__(self, backgroundX, backgroundY, backgroundW, backgroundH):
        quit_button = Button(name="Quit", xCoord=(backgroundX + (backgroundW / 2)), yCoord=(backgroundY + (backgroundH / 2)))
        quit_button.select()
        another_button = Button(name="Another", xCoord=quit_button.x, yCoord=quit_button.y - 55)
        Buttons.list.append(quit_button)
        Buttons.list.append(another_button)
        
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
    
    def __init__(self, name, xCoord, yCoord):
        super().__init__(name,
                         font_name='Times New Roman',
                         font_size=32,
                         x=xCoord,
                         y=yCoord,
                         color=(0, 0, 0, 255),
                         align='center',
                         anchor_x='center',
                         anchor_y='center')
        self.button_text = name
        
    def select(self):
        self.font_size = 48
        self.color = (50, 50, 50, 255)
        
    def deselect(self):
        self.font_size = 32  
        self.color = (0, 0, 0, 255)
        