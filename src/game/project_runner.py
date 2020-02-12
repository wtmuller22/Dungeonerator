import pyglet
from game.floor import Floor
from game.menu import Menu
from game.game_state import State
from pyglet.window import key
'''
Created on Feb 11, 2020

@author: Wyatt Muller

Project runner for Dungeonerator.
'''

window = pyglet.window.Window(fullscreen=True)
state = State.Menu
background = Floor(windowW=window.width, windowH=window.height)
menu = Menu(backgroundX=background.x, backgroundY=background.y, backgroundW=background.width, backgroundH=background.height)


def main():
    pyglet.app.run()
    
def select_button():
    selected = menu.get_current_idx()
    if (selected == 2):
        pyglet.app.exit()

@window.event
def on_draw():
    window.clear()
    background.draw()
    menu.draw()
    
@window.event
def on_key_press(symbol, modifiers):
    if state == State.Menu:
        if symbol == key.W:
            select_button()
        elif (symbol == key.DOWN or symbol == key.RIGHT):
            menu.next()
        elif (symbol == key.UP or symbol == key.LEFT):
            menu.previous()

if __name__ == '__main__':
    main()