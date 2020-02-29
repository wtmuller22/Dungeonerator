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
        self.text_by = Label("By: Wyatt Muller",
                              font_name='Cracked Johnnie',
                              font_size=16,
                              x=backgroundX + (backgroundW / 2) + 200,
                              y=backgroundY + (backgroundH / 2) + 120,
                              color=(0, 0, 0, 255),
                              align='center',
                              anchor_x='center',
                              anchor_y='center')
        self.text_bindings = Label("Key Bindings:",
                              font_name='Times New Roman',
                              font_size=16,
                              x=backgroundX + 900,
                              y=backgroundY + 80,
                              color=(0, 0, 0, 150),
                              align='center',
                              anchor_x='center',
                              anchor_y='center', 
                              bold=True)
        self.text_select = Label("Select: W",
                              font_name='Times New Roman',
                              font_size=16,
                              x=backgroundX + 900,
                              y=backgroundY + 60,
                              color=(0, 0, 0, 150),
                              align='center',
                              anchor_x='center',
                              anchor_y='center',
                              bold=True)
        self.text_arrows = Label("Scroll: Arrow Keys",
                              font_name='Times New Roman',
                              font_size=16,
                              x=backgroundX + 900,
                              y=backgroundY + 40,
                              color=(0, 0, 0, 150),
                              align='center',
                              anchor_x='center',
                              anchor_y='center',
                              bold=True)
        
    def draw(self):
        self.text_dungeonerator.draw()
        self.text_the.draw()
        self.text_by.draw()
        self.text_bindings.draw()
        self.text_select.draw()
        self.text_arrows.draw()