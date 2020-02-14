import pyglet
from game.floor import Floor
from game.menu import Menu
from game.game_state import State
from game.door import Door
from game.cardinal_direction import Direction
from game.player import Player
from pyglet.window import key
'''
Created on Feb 11, 2020

@author: Wyatt Muller

Project runner for Dungeonerator.
'''

window = pyglet.window.Window(fullscreen=True)
current_state = State.Menu
background = Floor(windowW=window.width, windowH=window.height)
startX = background.x
startY = background.y
menu = Menu(backgroundX=startX, backgroundY=startY, backgroundW=background.width, backgroundH=background.height)
door_west = Door(Direction.WEST, backgroundX=startX, backgroundY=startY)
door_north = Door(Direction.NORTH, backgroundX=startX, backgroundY=startY)
door_east = Door(Direction.EAST, backgroundX=startX, backgroundY=startY)
door_south = Door(Direction.SOUTH, backgroundX=startX, backgroundY=startY)
player1 = Player(given_name='player1', backgroundX=startX, backgroundY=startY)

def main():
    pyglet.app.run()
    
def select_button():
    selected = menu.get_current_idx()
    if (selected == 2):
        pyglet.app.exit()
    elif (selected == 0):
        menu_to_game()
        
def menu_to_game():
    global current_state 
    current_state = State.Game
    background.switch_image()
    #pyglet.clock.schedule_interval(update, 1/60.0)
    
def game_to_menu():
    global current_state
    current_state = State.Game
    background.switch_image()
    #pyglet.clock.unschedule(update)
    
#def update(dt):
    
def start_moving_player(dt):
    valid = check_player_legal_movement()
    if (valid):
        player1.start_moving()
        pyglet.clock.schedule_interval(moving_bounds_check, 1/100.0)
        
def set_player_last_valid():
    if (player1.facing == Direction.WEST):
        remainder = 40 - ((player1.x - startX) % 40)
        player1.x = player1.x + remainder
    elif (player1.facing == Direction.EAST):
        remainder = (player1.x - startX) % 40
        player1.x = player1.x - remainder
    elif (player1.facing == Direction.NORTH):
        remainder = (player1.y - startY) % 40
        player1.y = player1.y - remainder
    else:
        remainder = 40 - ((player1.y - startY) % 40)
        player1.y = player1.y + remainder
        
def moving_bounds_check(dt):
    valid = check_player_legal_movement()
    if (not valid):
        player1.stop_moving()
        set_player_last_valid()
        pyglet.clock.unschedule(moving_bounds_check)
    
def check_player_legal_movement() -> bool:
    if (player1.facing == Direction.WEST):
        return player1.x > startX
    elif (player1.facing == Direction.EAST):
        return player1.x < startX + background.width - 40
    elif (player1.facing == Direction.NORTH):
        return player1.y < startY + background.height - 40
    else:
        return player1.y > 0
    
def wait_until_player_in_box(dt):
    if (player1.facing == Direction.WEST):
        if (player1.x <= player1.nextBoxCoord):
            player1.stop_moving()
            player1.x = player1.nextBoxCoord
            pyglet.clock.unschedule(wait_until_player_in_box)
            if (not player1.queued_direction is None):
                player1.change_direction(player1.queued_direction)
                start_moving_player(dt)
                player1.queued_direction = None
    elif (player1.facing == Direction.EAST):
        if (player1.x >= player1.nextBoxCoord):
            player1.stop_moving()
            player1.x = player1.nextBoxCoord
            pyglet.clock.unschedule(wait_until_player_in_box)
            if (not player1.queued_direction is None):
                player1.change_direction(player1.queued_direction)
                start_moving_player(dt)
                player1.queued_direction = None
    elif (player1.facing == Direction.NORTH):
        if (player1.y >= player1.nextBoxCoord):
            player1.stop_moving()
            player1.y = player1.nextBoxCoord
            pyglet.clock.unschedule(wait_until_player_in_box)
            if (not player1.queued_direction is None):
                player1.change_direction(player1.queued_direction)
                start_moving_player(dt)
                player1.queued_direction = None
    else:
        if (player1.y <= player1.nextBoxCoord):
            player1.stop_moving()
            player1.y = player1.nextBoxCoord
            pyglet.clock.unschedule(wait_until_player_in_box)
            if (not player1.queued_direction is None):
                player1.change_direction(player1.queued_direction)
                start_moving_player(dt)
                player1.queued_direction = None
    
def set_next_box_coords():
    if (player1.facing == Direction.WEST):
        player1.nextBoxCoord = player1.x - ((player1.x - startX) % 40)
    elif (player1.facing == Direction.EAST):
        player1.nextBoxCoord = player1.x + (40 - ((player1.x - startX) % 40))
    elif (player1.facing == Direction.NORTH):
        player1.nextBoxCoord = player1.y + (40 - ((player1.y - startY) % 40))
    else:
        player1.nextBoxCoord = player1.y - ((player1.y - startY) % 40)

@window.event
def on_draw():
    window.clear()
    background.draw()
    if (current_state == State.Menu):
        menu.draw()
    if (current_state == State.Game):
        door_west.draw()
        door_north.draw()
        door_east.draw()
        door_south.draw()
        player1.draw()
    
@window.event
def on_key_press(symbol, modifiers):
    if current_state == State.Menu:
        if symbol == key.W:
            select_button()
        elif (symbol == key.DOWN or symbol == key.RIGHT):
            menu.next()
        elif (symbol == key.UP or symbol == key.LEFT):
            menu.previous()
    elif current_state == State.Game:
        if (not player1.is_moving):
            player1.queued_direction = None
            if symbol == key.UP:
                player1.change_direction(Direction.NORTH)
                pyglet.clock.schedule_once(start_moving_player, 0.10)
            elif symbol == key.RIGHT:
                player1.change_direction(Direction.EAST)
                pyglet.clock.schedule_once(start_moving_player, 0.10)
            elif symbol == key.DOWN:
                player1.change_direction(Direction.SOUTH)
                pyglet.clock.schedule_once(start_moving_player, 0.10)
            elif symbol == key.LEFT:
                player1.change_direction(Direction.WEST)
                pyglet.clock.schedule_once(start_moving_player, 0.10)
        else:
            if symbol == key.UP:
                player1.queued_direction = Direction.NORTH
            elif symbol == key.RIGHT:
                player1.queued_direction = Direction.EAST
            elif symbol == key.LEFT:
                player1.queued_direction = Direction.WEST
            elif symbol == key.DOWN:
                player1.queued_direction = Direction.SOUTH
            
@window.event
def on_key_release(symbol, modifiers):
    if (current_state == State.Game):
        if ((symbol == key.UP and player1.facing == Direction.NORTH) or (symbol == key.RIGHT and player1.facing == Direction.EAST) or (symbol == key.DOWN and player1.facing == Direction.SOUTH) or (symbol == key.LEFT and player1.facing == Direction.WEST)):
            pyglet.clock.unschedule(start_moving_player)
            if (player1.is_moving):
                set_next_box_coords()
                pyglet.clock.schedule_interval(wait_until_player_in_box, 1/100.0)
        if ((symbol == key.UP and player1.queued_direction == Direction.NORTH) or (symbol == key.RIGHT and player1.queued_direction == Direction.EAST) or (symbol == key.DOWN and player1.queued_direction == Direction.SOUTH) or (symbol == key.LEFT and player1.queued_direction == Direction.WEST)):
            player1.queued_direction = None

if __name__ == '__main__':
    main()