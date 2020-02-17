import pyglet
from game.floor import Floor
from game.menu import Menu
from game.game_state import State
from game.door import Door
from game.cardinal_direction import Direction
from game.player import Player
from game.map import Map
from game.level import Level
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
displayed_level = Level(backgroundX=startX, backgroundY=startY)

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
    current_room = room_map.change_to_room(number=0, level=0)
    current_state = State.Game
    background.switch_image()
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
            player1.y = player1.y + 960
    elif (room_location == Direction.NE):
        if (player_facing == Direction.WEST):
            player1.room_number = player1.room_number - 1
            player1.x = player1.x + 960
        elif (player_facing == Direction.SOUTH):
            player1.room_number = player1.room_number + 1
            player1.y = player1.y + 960
    elif (room_location == Direction.SE):
        if (player_facing == Direction.NORTH):
            player1.room_number = player1.room_number - 1
            player1.y = player1.y - 960
        elif (player_facing == Direction.WEST):
            player1.room_number = player1.room_number + 1
            player1.x = player1.x + 960
    elif (room_location == Direction.SW):
        if (player_facing == Direction.EAST):
            player1.room_number = player1.room_number - 1
            player1.x = player1.x - 960
        elif (player_facing == Direction.NORTH):
            player1.room_number = player1.room_number + 1
            player1.y = player1.y - 960
    elif (room_location == Direction.NORTH):
        if (player_facing == Direction.EAST):
            player1.room_number = player1.room_number + 1
            player1.x = player1.x - 960
        elif (player_facing == Direction.WEST):
            player1.room_number = player1.room_number - 1
            player1.x = player1.x + 960
    elif (room_location == Direction.EAST):
        if (player_facing == Direction.NORTH):
            player1.room_number = player1.room_number - 1
            player1.y = player1.y - 960
        elif (player_facing == Direction.SOUTH):
            player1.room_number = player1.room_number + 1
            player1.y = player1.y + 960
    elif (room_location == Direction.SOUTH):
        if (player_facing == Direction.EAST):
            player1.room_number = player1.room_number - 1
            player1.x = player1.x - 960
        elif (player_facing == Direction.WEST):
            player1.room_number = player1.room_number + 1
            player1.x = player1.x + 960
    else:
        if (player_facing == Direction.NORTH):
            num_rooms_per_side = (player1.level * 2) + 1
            if (player1.room_number == ((num_rooms_per_side**2) - 1)):
                player1.room_number = (((player1.level - 1) * 2) + 1)**2
            else:
                player1.room_number = player1.room_number + 1
            player1.y = player1.y - 960
        elif (player_facing == Direction.SOUTH):
            player1.room_number = player1.room_number - 1
            player1.y = player1.y + 960
    current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
    
def change_player_level():
    global current_room
    global player1
    global displayed_level
    room_location = current_room.location
    player_facing = player1.facing
    if ((room_location == Direction.NW or room_location == Direction.NORTH or room_location == Direction.NE) and (player_facing == Direction.NORTH)):
        result = room_map.level_prepared(level=(player1.level + 1))
        door = None
        if (not result):
            room_map.prepare_level(level_num=(player1.level + 1))
            door = Door(direct=Direction.SOUTH, backgroundX=startX, backgroundY=startY)
            door.make_golden()
        player1.room_number = player1.room_number + (8 * player1.level) + 1
        player1.level = player1.level + 1
        current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
        player1.y = player1.y - 960
        if (not door is None):
            current_room.entities.append(door)
    elif ((room_location == Direction.NW or room_location == Direction.WEST or room_location == Direction.SW) and (player_facing == Direction.WEST)):
        result = room_map.level_prepared(level=(player1.level + 1))
        door = None
        if (not result):
            room_map.prepare_level(level_num=(player1.level + 1))
            door = Door(direct=Direction.EAST, backgroundX=startX, backgroundY=startY)
            door.make_golden()
        player1.room_number = player1.room_number + (8 * player1.level) + 7
        player1.level = player1.level + 1
        current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
        player1.x = player1.x + 960
        if (not door is None):
            current_room.entities.append(door)
    elif ((room_location == Direction.SW or room_location == Direction.SOUTH or room_location == Direction.SE) and (player_facing == Direction.SOUTH)):
        result = room_map.level_prepared(level=(player1.level + 1))
        door = None
        if (not result):
            room_map.prepare_level(level_num=(player1.level + 1))
            door = Door(direct=Direction.NORTH, backgroundX=startX, backgroundY=startY)
            door.make_golden()
        player1.room_number = player1.room_number + (8 * player1.level) + 5
        player1.level = player1.level + 1
        current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
        player1.y = player1.y + 960
        if (not door is None):
            current_room.entities.append(door)
    elif ((room_location == Direction.NE or room_location == Direction.EAST or room_location == Direction.SE) and (player_facing == Direction.EAST)):
        result = room_map.level_prepared(level=(player1.level + 1))
        door = None
        if (not result):
            room_map.prepare_level(level_num=(player1.level + 1))
            door = Door(direct=Direction.WEST, backgroundX=startX, backgroundY=startY)
            door.make_golden()
        player1.room_number = player1.room_number + (8 * player1.level) + 3
        player1.level = player1.level + 1
        current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
        player1.x = player1.x - 960
        if (not door is None):
            current_room.entities.append(door)
    elif ((room_location == Direction.NORTH) and (player_facing == Direction.SOUTH)):
        player1.level = player1.level - 1
        player1.room_number = player1.room_number - ((8 * player1.level) + 1)
        if (player1.level == 0):
            player1.room_number = 0
        current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
        player1.y = player1.y + 960
    elif ((room_location == Direction.EAST) and (player_facing == Direction.WEST)):
        player1.level = player1.level - 1
        player1.room_number = player1.room_number - ((8 * player1.level) + 3)
        if (player1.level == 0):
            player1.room_number = 0
        current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
        player1.x = player1.x + 960
    elif ((room_location == Direction.SOUTH) and (player_facing == Direction.NORTH)):
        player1.level = player1.level - 1
        player1.room_number = player1.room_number - ((8 * player1.level) + 5)
        if (player1.level == 0):
            player1.room_number = 0
        current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
        player1.y = player1.y - 960
    elif ((room_location == Direction.WEST) and (player_facing == Direction.EAST)):
        player1.level = player1.level - 1
        player1.room_number = player1.room_number - ((8 * player1.level) + 7)
        if (player1.level == 0):
            player1.room_number = 0
        current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
        player1.x = player1.x - 960
    else:
        if (player_facing == Direction.NORTH):
            result = room_map.level_prepared(level=(player1.level + 1))
            door = None
            if (not result):
                room_map.prepare_level(level_num=(player1.level + 1))
                door = Door(direct=Direction.SOUTH, backgroundX=startX, backgroundY=startY)
                door.make_golden()
            player1.room_number = player1.room_number + 2
            player1.level = player1.level + 1
            current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
            player1.y = player1.y - 960
            if (not door is None):
                current_room.entities.append(door)
        elif (player_facing == Direction.EAST):
            result = room_map.level_prepared(level=(player1.level + 1))
            door = None
            if (not result):
                room_map.prepare_level(level_num=(player1.level + 1))
                door = Door(direct=Direction.WEST, backgroundX=startX, backgroundY=startY)
                door.make_golden()
            player1.room_number = player1.room_number + 4
            player1.level = player1.level + 1
            current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
            player1.x = player1.x - 960
            if (not door is None):
                current_room.entities.append(door)
        elif (player_facing == Direction.SOUTH):
            result = room_map.level_prepared(level=(player1.level + 1))
            door = None
            if (not result):
                room_map.prepare_level(level_num=(player1.level + 1))
                door = Door(direct=Direction.NORTH, backgroundX=startX, backgroundY=startY)
                door.make_golden()
            player1.room_number = player1.room_number + 6
            player1.level = player1.level + 1
            current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
            player1.y = player1.y + 960
            if (not door is None):
                current_room.entities.append(door)
        else:
            result = room_map.level_prepared(level=(player1.level + 1))
            door = None
            if (not result):
                room_map.prepare_level(level_num=(player1.level + 1))
                door = Door(direct=Direction.EAST, backgroundX=startX, backgroundY=startY)
                door.make_golden()
            player1.room_number = player1.room_number + 8
            player1.level = player1.level + 1
            current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
            player1.x = player1.x + 960
            if (not door is None):
                current_room.entities.append(door)
    displayed_level.update_level(new_level=player1.level)
    
def start_moving_player(dt):
    set_next_box_coords()
    valid = check_player_legal_movement()
    if (valid):
        player1.start_moving()
        pyglet.clock.schedule_interval(moving_bounds_check, 1/100.0)
        
def set_player_last_valid():
    if (player1.facing == Direction.WEST):
        if (player1.x <= startX):
            remainder = 40 - ((player1.x - startX) % 40)
            player1.x = player1.x + remainder
        else:
            if (player1.x != player1.nextBoxCoord):
                player1.x = player1.nextBoxCoord + 40
    elif (player1.facing == Direction.EAST):
        if (player1.x < startX + background.width - 40):
            remainder = (player1.x - startX) % 40
            player1.x = player1.x - remainder
        else:
            if (player1.x != player1.nextBoxCoord):
                player1.x = player1.nextBoxCoord - 40
    elif (player1.facing == Direction.NORTH):
        if (player1.y < startY + background.height - 40):
            remainder = (player1.y - startY) % 40
            player1.y = player1.y - remainder
        else:
            if (player1.y != player1.nextBoxCoord):
                player1.y = player1.nextBoxCoord - 40
    else:
        if (player1.y > 0):
            remainder = 40 - ((player1.y - startY) % 40)
            player1.y = player1.y + remainder
        else:
            if (player1.y != player1.nextBoxCoord):
                player1.y = player1.nextBoxCoord + 40
        
def moving_bounds_check(dt):
    set_next_box_coords()
    valid = check_player_legal_movement()
    if (not valid):
        player1.stop_moving()
        set_player_last_valid()
        pyglet.clock.unschedule(moving_bounds_check)
    
def check_player_legal_movement() -> bool:
    if (player1.facing == Direction.WEST):
        result = player1.x > startX
        check_x = player1.nextBoxCoord
        if (check_x == player1.x):
            check_x = check_x - 40
        is_monster = current_room.is_monster(aX=(check_x), aY=(player1.y))
        if (not result):
            door = current_room.intersecting_door(playerX=player1.x, playerY=player1.y)
            if (not door is None):
                is_golden = door.is_level_up()
                if (not is_golden):
                    change_player_room()
                else:
                    change_player_level()
        return result and (not is_monster)
    elif (player1.facing == Direction.EAST):
        result = player1.x < startX + background.width - 40
        check_x = player1.nextBoxCoord
        if (check_x == player1.x):
            check_x = check_x + 40
        is_monster = current_room.is_monster(aX=(check_x), aY=(player1.y))
        if (not result):
            door = current_room.intersecting_door(playerX=player1.x, playerY=player1.y)
            if (not door is None):
                is_golden = door.is_level_up()
                if (not is_golden):
                    change_player_room()
                else:
                    change_player_level()
        return result and (not is_monster)
    elif (player1.facing == Direction.NORTH):
        result = player1.y < startY + background.height - 40
        check_y = player1.nextBoxCoord
        if (check_y == player1.y):
            check_y = check_y + 40
        is_monster = current_room.is_monster(aX=(player1.x), aY=(check_y))
        if (not result):
            door = current_room.intersecting_door(playerX=player1.x, playerY=player1.y)
            if (not door is None):
                is_golden = door.is_level_up()
                if (not is_golden):
                    change_player_room()
                else:
                    change_player_level()
        return result and (not is_monster)
    else:
        result = player1.y > 0
        check_y = player1.nextBoxCoord
        if (check_y == player1.y):
            check_y = check_y - 40
        is_monster = current_room.is_monster(aX=(player1.x), aY=(check_y))
        if (not result):
            door = current_room.intersecting_door(playerX=player1.x, playerY=player1.y)
            if (not door is None):
                is_golden = door.is_level_up()
                if (not is_golden):
                    change_player_room()
                else:
                    change_player_level()
        return result and (not is_monster)
    
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
        displayed_level.draw()
    
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
                pyglet.clock.unschedule(moving_bounds_check)
                set_next_box_coords()
                pyglet.clock.schedule_interval(wait_until_player_in_box, 1/100.0)
        if ((symbol == key.UP and player1.queued_direction == Direction.NORTH) or (symbol == key.RIGHT and player1.queued_direction == Direction.EAST) or (symbol == key.DOWN and player1.queued_direction == Direction.SOUTH) or (symbol == key.LEFT and player1.queued_direction == Direction.WEST)):
            player1.queued_direction = None

if __name__ == '__main__':
    main()