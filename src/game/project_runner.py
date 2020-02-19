import pyglet
from game.floor import Floor
from game.menu import Menu
from game.game_state import State
from game.door import Door
from game.cardinal_direction import Direction
from game.player import Player
from game.map import Map
from game.level import Level
from game.gameover import GameOver
from game.visibility import Visibility
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
visibility = Visibility()
player1 = Player(given_name='player1', backgroundX=startX, backgroundY=startY, darkness=visibility)
room_map = Map(backgroundX=startX, backgroundY=startY)
current_room = None
displayed_level = Level(backgroundX=startX, backgroundY=startY)
game_over = GameOver(backgroundX=startX, backgroundY=startY)
player_is_alive = True

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
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.clock.schedule_interval(check_ground, 1/60.0)
    
def inventory_to_menu():
    global current_state
    global current_room
    current_state = State.Menu
    background.switch_image()
    current_room = None
    pyglet.clock.unschedule(update)
    pyglet.clock.unschedule(check_ground)
    
def game_to_inventory():
    global current_state
    current_state = State.Inventory
    
def inventory_to_game():
    global current_state
    current_state = State.Game
    
def player_died():
    global player_is_alive
    player_is_alive = False
    player1.fade()
    game_over.color = (140, 0, 0, 255)   
    pyglet.clock.unschedule(update) 
    pyglet.clock.unschedule(check_ground)
    
def check_ground(dt):
    if (not current_room is None):
        result = current_room.intersecting_item(playerX=player1.x, playerY=player1.y)
        visibility.update_coords(aX=(player1.x + 20), aY=(player1.y + 20))
        if (not result is None):
            ground_type = result.item_enum
            add_result = player1.add_to_inventory(to_add=ground_type)
            if (add_result):
                result.remove_self()
    
def update(dt):
    if (not current_room is None):
        if (player1.is_moving):
            if (player1.facing == Direction.NORTH or player1.facing == Direction.SOUTH):
                total_damage = current_room.update(dt, playerX=player1.x, playerY=player1.nextBoxCoord)
                if (total_damage > 0):
                    is_dead = player1.change_life(-1 * total_damage)
                    if (is_dead):
                        player_died()
            else:
                total_damage = current_room.update(dt, playerX=player1.nextBoxCoord, playerY=player1.y)
                if (total_damage > 0):
                    is_dead = player1.change_life(-1 * total_damage)
                    if (is_dead):
                        player_died()
        else:
            total_damage = current_room.update(dt, playerX=player1.x, playerY=player1.y)
            if (total_damage > 0):
                    is_dead = player1.change_life(-1 * total_damage)
                    if (is_dead):
                        player_died()

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
            player1.x = startX
        else:
            if (player1.x != player1.nextBoxCoord):
                player1.x = player1.nextBoxCoord + 40
    elif (player1.facing == Direction.EAST):
        if (player1.x >= startX + background.width - 40):
            player1.x = startX + background.width - 40
        else:
            if (player1.x != player1.nextBoxCoord):
                player1.x = player1.nextBoxCoord - 40
    elif (player1.facing == Direction.NORTH):
        if (player1.y >= startY + background.height - 40):
            player1.y = startY + background.height - 40
        else:
            if (player1.y != player1.nextBoxCoord):
                player1.y = player1.nextBoxCoord - 40
    else:
        if (player1.y <= startY):
            player1.y = startY
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
        
def player_attack():
    if player1.attack > 0 and not player1.is_attacking:
        player1.is_attacking = True
        pyglet.clock.schedule_once(player1.stop_attack, 0.75)
        player1.attack_sprite.reset_animation()
        if player1.facing == Direction.NORTH:
            check_y = player1.nextBoxCoord
            if (check_y == player1.y):
                check_y = check_y + 40
            current_room.player_attack(damage=player1.attack, playerX=player1.x, playerY=check_y)
        elif player1.facing == Direction.EAST:
            check_x = player1.nextBoxCoord
            if (check_x == player1.x):
                check_x = check_x + 40
            current_room.player_attack(damage=player1.attack, playerX=check_x, playerY=player1.y)
        elif player1.facing == Direction.SOUTH:
            check_y = player1.nextBoxCoord
            if (check_y == player1.y):
                check_y = check_y - 40
            current_room.player_attack(damage=player1.attack, playerX=player1.x, playerY=check_y)
        else:
            check_x = player1.nextBoxCoord
            if (check_x == player1.x):
                check_x = check_x - 40
            current_room.player_attack(damage=player1.attack, playerX=check_x, playerY=player1.y)

@window.event
def on_draw():
    window.clear()
    background.draw()
    if (current_state == State.Menu):
        menu.draw()
    if (current_state == State.Game or current_state == State.Inventory):
        current_room.draw()
        visibility.draw()
        player1.draw()
        displayed_level.draw()
        game_over.draw()
    if (current_state == State.Inventory and player_is_alive):
        player1.draw_inventory()
    
@window.event
def on_key_press(symbol, modifiers):
    if current_state == State.Menu:
        if symbol == key.W:
            select_button()
        elif (symbol == key.DOWN or symbol == key.RIGHT):
            menu.next()
        elif (symbol == key.UP or symbol == key.LEFT):
            menu.previous()
    elif current_state == State.Game and player_is_alive:
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
        if symbol == key.E:
            player1.queued_direction = None
            pyglet.clock.unschedule(start_moving_player)
            if (player1.is_moving):
                pyglet.clock.unschedule(moving_bounds_check)
                set_next_box_coords()
                pyglet.clock.schedule_interval(wait_until_player_in_box, 1/100.0)
            game_to_inventory()
        if symbol == key.W:
            player_attack()
    elif current_state == State.Inventory and player_is_alive:
        if symbol == key.UP:
            player1.change_highlight(direc=Direction.NORTH)
        elif symbol == key.RIGHT:
            player1.change_highlight(direc=Direction.EAST)
        elif symbol == key.DOWN:
            player1.change_highlight(direc=Direction.SOUTH)
        elif symbol == key.LEFT:
            player1.change_highlight(direc=Direction.WEST)
        elif symbol == key.W:
            player1.toggle_select_highlight()
        elif symbol == key.E:
            inventory_to_game()
            
@window.event
def on_key_release(symbol, modifiers):
    if (current_state == State.Game and player_is_alive):
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