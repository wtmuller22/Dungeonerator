import pyglet
from game.floor import Floor
from game.menu import Menu
from game.game_state import State
from game.door import Door
from game.cardinal_direction import Direction
from game.player import Player
from game.map import Map
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
player1 = Player(given_name='player1', backgroundX=startX, backgroundY=startY)
room_map = Map(backgroundX=startX, backgroundY=startY)
current_room = None

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
    global current_room
    current_state = State.Game
    background.switch_image()
    current_room = room_map.change_to_room(number=0)
    #pyglet.clock.schedule_interval(update, 1/60.0)
    
def game_to_menu():
    global current_state
    global current_room
    current_state = State.Game
    background.switch_image()
    current_room = None
    #pyglet.clock.unschedule(update)
    
#def update(dt):

def change_player_room():
    global current_room
    room_location = current_room.location
    player_facing = player1.facing
    if (room_location == Direction.NW):
        if (player_facing == Direction.EAST):
            player1.room_number = player1.room_number + 1
            player1.x = player1.x - 960
        elif (player_facing == Direction.SOUTH):
            num_rooms_per_side = (player1.level * 2) + 1
            player1.room_number = (num_rooms_per_side**2) - 1
    elif (room_location == Direction.NE):
        if (player_facing == Direction.WEST):
            player1.room_number = player1.room_number - 1
        elif (player_facing == Direction.SOUTH):
            player1.room_number = player1.room_number + 1
    elif (room_location == Direction.SE):
        if (player_facing == Direction.NORTH):
            player1.room_number = player1.room_number - 1
        elif (player_facing == Direction.WEST):
            player1.room_number = player1.room_number + 1
    elif (room_location == Direction.SW):
        if (player_facing == Direction.EAST):
            player1.room_number = player1.room_number - 1
        elif (player_facing == Direction.NORTH):
            player1.room_number = player1.room_number + 1
    elif (room_location == Direction.NORTH):
        if (player_facing == Direction.EAST):
            player1.room_number = player1.room_number + 1
        elif (player_facing == Direction.WEST):
            player1.room_number = player1.room_number - 1
    elif (room_location == Direction.EAST):
        if (player_facing == Direction.NORTH):
            player1.room_number = player1.room_number - 1
        elif (player_facing == Direction.SOUTH):
            player1.room_number = player1.room_number + 1
    elif (room_location == Direction.SOUTH):
        if (player_facing == Direction.EAST):
            player1.room_number = player1.room_number - 1
        elif (player_facing == Direction.WEST):
            player1.room_number = player1.room_number + 1
    else:
        if (player_facing == Direction.NORTH):
            num_rooms_per_side = (player1.level * 2) + 1
            if (player1.room_number == ((num_rooms_per_side**2) - 1)):
                player1.room_number = (((player1.level - 1) * 2) + 1)**2
            else:
                player1.room_number = player1.room_number + 1
        elif (player_facing == Direction.SOUTH):
            player1.room_number = player1.room_number - 1
    current_room = room_map.change_to_room(number=player1.room_number)
    
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
        result = player1.x > startX
        if (not result):
            door = current_room.intersecting_door(playerX=player1.x, playerY=player1.y)
            if (not door is None):
                is_golden = door.is_level_up()
                if (not is_golden):
                    change_player_room()
                else:
                    change_player_level()
        return result
    elif (player1.facing == Direction.EAST):
        result = player1.x < startX + background.width - 40
        return result
    elif (player1.facing == Direction.NORTH):
        result = player1.y < startY + background.height - 40
        return result
    else:
        result = player1.y > 0
        return result
    
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
        current_room.draw()
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