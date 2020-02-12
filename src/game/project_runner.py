import pyglet
from game.floor import Floor
from game.buttons import Buttons
from game.game_state import State
from pyglet.window import key
'''
Created on Feb 11, 2020

@author: Wyatt Muller

Project runner for Dungeonerator.
'''

window = pyglet.window.Window(fullscreen=True)
state = State.Menu
background = Floor()
menu_buttons = Buttons(backgroundX=background.x, backgroundY=background.y, backgroundW=background.width, backgroundH=background.height)

def main():
    pyglet.app.run()
    
def select_button():
    selected = menu_buttons.current_idx
    if (selected == 0):
        pyglet.app.exit()

@window.event
def on_draw():
    window.clear()
    background.draw()
    menu_buttons.draw()
    
@window.event
def on_key_press(symbol, modifiers):
    if state == State.Menu:
        if symbol == key.W:
            select_button()
        elif (symbol == key.DOWN or symbol == key.RIGHT):
            menu_buttons.next()
        elif (symbol == key.UP or symbol == key.LEFT):
            menu_buttons.previous()

if __name__ == '__main__':
    main()