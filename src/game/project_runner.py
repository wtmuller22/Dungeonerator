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
from game.room import Monster
from game.room import Item
from game.room import Room
from game.player import Item as pItem
from game.item_type import Type
from game.player import Rarity
from game import room
'''
Created on Feb 11, 2020

@author: Wyatt Muller

Project runner for Dungeonerator.
'''

window = pyglet.window.Window(fullscreen=True)
window.set_mouse_visible(visible=False)
current_state = State.Menu
background = Floor(windowW=window.width, windowH=window.height)
startX = background.x
startY = background.y
menu = Menu(backgroundX=startX, backgroundY=startY, backgroundW=background.width, backgroundH=background.height)
visibility = Visibility()
player1 = Player(given_name='player1', backgroundX=startX, backgroundY=startY, darkness=visibility)
room_map = Map(backgroundX=startX, backgroundY=startY)
current_room = room_map.change_to_room(number=0, level=0)
displayed_level = Level(backgroundX=startX, backgroundY=startY)
game_over = GameOver(backgroundX=startX, backgroundY=startY)
player_is_alive = True

def main():
    pyglet.app.run()
    
def reset_data():
    global visibility
    global player1
    global room_map
    global displayed_level
    global game_over
    global player_is_alive
    global current_room
    visibility = Visibility()
    player1 = Player(given_name='player1', backgroundX=startX, backgroundY=startY, darkness=visibility)
    room_map = Map(backgroundX=startX, backgroundY=startY)
    displayed_level = Level(backgroundX=startX, backgroundY=startY)
    game_over = GameOver(backgroundX=startX, backgroundY=startY)
    player_is_alive = True
    current_room = room_map.change_to_room(number=0, level=0)
    
def select_button():
    selected = menu.get_current_idx()
    if (selected == 2):
        pyglet.app.exit()
    elif (selected == 0):
        menu_to_game()
    elif (selected == 1):
        load_state()
        menu_to_game()
        
def menu_to_game():
    global current_state 
    global current_room
    current_state = State.Game
    background.switch_image()
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.clock.schedule_interval(check_ground, 1/60.0)
    
def inventory_to_menu():
    global current_state
    current_state = State.Menu
    background.switch_image()
    pyglet.clock.unschedule(update)
    pyglet.clock.unschedule(check_ground)
    reset_data()
    
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
    game_over.make_visible()
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
            player1.add_experience(exp=(5 * (player1.level + 1)))
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
            player1.add_experience(exp=(5 * (player1.level + 1)))
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
            player1.add_experience(exp=(5 * (player1.level + 1)))
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
            player1.add_experience(exp=(5 * (player1.level + 1)))
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
                player1.add_experience(exp=(5 * (player1.level + 1)))
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
                player1.add_experience(exp=(5 * (player1.level + 1)))
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
                player1.add_experience(exp=(5 * (player1.level + 1)))
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
                player1.add_experience(exp=(5 * (player1.level + 1)))
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
    player1.scheduled_moving = False
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
            total_exp = current_room.player_attack(damage=player1.attack, playerX=player1.x, playerY=check_y)
            result = player1.selected_weapon.take_damage(damage=10)
            player1.add_experience(exp=total_exp)
            if (result):
                player1.selected_weapon = None
        elif player1.facing == Direction.EAST:
            check_x = player1.nextBoxCoord
            if (check_x == player1.x):
                check_x = check_x + 40
            total_exp = current_room.player_attack(damage=player1.attack, playerX=check_x, playerY=player1.y)
            result = player1.selected_weapon.take_damage(damage=10)
            player1.add_experience(exp=total_exp)
            if (result):
                player1.selected_weapon = None
        elif player1.facing == Direction.SOUTH:
            check_y = player1.nextBoxCoord
            if (check_y == player1.y):
                check_y = check_y - 40
            total_exp = current_room.player_attack(damage=player1.attack, playerX=player1.x, playerY=check_y)
            result = player1.selected_weapon.take_damage(damage=10)
            player1.add_experience(exp=total_exp)
            if (result):
                player1.selected_weapon = None
        else:
            check_x = player1.nextBoxCoord
            if (check_x == player1.x):
                check_x = check_x - 40
            total_exp = current_room.player_attack(damage=player1.attack, playerX=check_x, playerY=player1.y)
            result = player1.selected_weapon.take_damage(damage=10)
            player1.add_experience(exp=total_exp)
            if (result):
                player1.selected_weapon = None
                
def save_state():
    with open('saves/player.txt', 'w', encoding = 'utf-8') as f:
        f.write('Name: ' + player1.name + '\n')
        f.write('X: ' + str(player1.x) + '\n')
        f.write('Y: ' + str(player1.y) + '\n')
        f.write('Next Coord: ' + str(player1.nextBoxCoord) + '\n')
        f.write('Level: ' + str(player1.level) + '\n')
        f.write('Room Number: ' + str(player1.room_number) + '\n')
        f.write('Next Stat: ' + str(player1.next_up_stat) + '\n')
        f.write('Defense: ' + str(player1.defense) + '\n')
        f.write('Speed: ' + str(player1.speed) + '\n')
        f.write('Attack: ' + str(player1.attack) + '\n')
        f.write('Facing: ' + str(player1.facing) + '\n')
        f.write('Number Hearts: ' + str(len(player1.life.life_array)) + '\n')
        life_missing = 0
        for heart in player1.life.life_array:
            life_missing = life_missing + (20 - heart.life)
        f.write('Missing Health: ' + str(life_missing) + '\n')
        f.write('Total Experience: ' + str(player1.experience.total_exp) + '\n')
        f.write('Exp Scale: ' + str(player1.experience.exp.scale) + '\n')
        f.write('Inventory Highlight X: ' + str(player1.player_inventory.highlighted_x) + '\n')
        f.write('Inventory Highlight Y: ' + str(player1.player_inventory.highlighted_y) + '\n')
        f.write('Visibility Scale: ' + str(player1.visibility.scale) + '\n')
        extra_slots = 0
        row_num = 0
        for row in player1.player_inventory.array:
            if (row_num > 1):
                extra_slots = extra_slots + len(row)
            row_num = row_num + 1
        f.write('Extra Slots: ' + str(extra_slots) + '\n')
        for row in player1.player_inventory.array:
            for slot in row:
                f.write('Slot:\n')
                f.write('Item:\n')
                if (slot.item is None):
                    f.write('None\n')
                else:
                    f.write('Type: ' + str(slot.item.type) + '\n')
                    f.write('Value: ' + str(slot.item.attack_strength_defense) + '\n')
                    f.write('Durability Max: ' + str(slot.item.durability_max) + '\n')
                    f.write('Durability: ' + str(slot.item.durability) + '\n')
                    f.write('Rarity: ' + str(slot.item.rarity) + '\n')
                f.write('Selected: ' + str(slot.is_selected) + '\n')
                f.write('Highlighted: ' + str(slot.is_highlighted) + '\n')
    with open('saves/map.txt', 'w', encoding = 'utf-8') as f:
        f.write('Room Dictionary:\n')
        keys = list(room_map.room_dict.keys())
        for key in keys:
            f.write('Room Number: ' + str(key) + '\n')
            this_room = room_map.room_dict[key]
            f.write('Direction: ' + str(this_room.location) + '\n')
            f.write('Level: ' + str(this_room.level) + '\n')
            f.write('Entities:\n')
            for entity in this_room.entities:
                if isinstance(entity, Monster):
                    f.write('Monster:\n')
                    f.write('Monster Type: ' + entity.monster_type + '\n')
                    f.write('Multiplier: ' + str(entity.multiplier) + '\n')
                    f.write('Health: ' + str(entity.health) + '\n')
                    f.write('Speed: ' + str(entity.speed) + '\n')
                    f.write('Attack: ' + str(entity.attack) + '\n')
                    f.write('Sight: ' + str(entity.sight) + '\n')
                    f.write('Is Moving: ' + str(entity.is_moving) + '\n')
                    f.write('Facing: ' + str(entity.facing) + '\n')
                    f.write('X: ' + str(entity.x) + '\n')
                    f.write('Y: ' + str(entity.y) + '\n')
                    f.write('Next Coord: ' + str(entity.next_coord) + '\n')
                elif isinstance(entity, Item):
                    f.write('Item:\n')
                    f.write('X: ' + str(entity.x) + '\n')
                    f.write('Y: ' + str(entity.y) + '\n')
                    f.write('Item Type: ' + str(entity.item_enum) + '\n')
                elif isinstance(entity, Door):
                    f.write('Door:\n')
                    f.write('X: ' + str(entity.x) + '\n')
                    f.write('Y: ' + str(entity.y) + '\n')
                    f.write('Is Gold: ' + str(entity.is_gold) + '\n')
                    f.write('Rotation: ' + str(entity.rotation) + '\n')
        f.write('Corner Dictionary:\n')
        keys = list(room_map.corner_numbers.keys())
        for key in keys:
            if key != 0:
                f.write('Corners:\n')
                f.write('Level: ' + str(key) + '\n')
                nums = room_map.corner_numbers[key]
                f.write('Corner: ' + str(nums[0]) + '\n')
                f.write('Corner: ' + str(nums[1]) + '\n')
                f.write('Corner: ' + str(nums[2]) + '\n')
                f.write('Corner: ' + str(nums[3]) + '\n')
                
def load_state():
    global current_room
    with open('saves/player.txt', 'r', encoding = 'utf-8') as f:
        row = 0
        slot = 0
        for line in f:
            if (line.startswith('Name:')):
                data = line[6:(len(line) - 1)]
                player1.name = data
            elif (line.startswith('X:')):
                data = line[3:(len(line) - 1)]
                player1.x = float(data)
            elif (line.startswith('Y:')):
                data = line[3:(len(line) - 1)]
                player1.y = float(data)
            elif (line.startswith('Next Coord:')):
                data = line[12:(len(line) - 1)]
                player1.nextBoxCoord = float(data)
            elif (line.startswith('Level:')):
                data = line[7:(len(line) - 1)]
                player1.level = int(data)
            elif (line.startswith('Room Number:')):
                data = line[13:(len(line) - 1)]
                player1.room_number = int(data)
            elif (line.startswith('Next Stat:')):
                data = line[11:(len(line) - 1)]
                player1.next_up_stat = int(data)
            elif (line.startswith('Defense:')):
                data = line[9:(len(line) - 1)]
                player1.defense = float(data)
            elif (line.startswith('Speed:')):
                data = line[7:(len(line) - 1)]
                player1.speed = int(data)
            elif (line.startswith('Attack:')):
                data = line[8:(len(line) - 1)]
                player1.attack = int(data)
            elif (line.startswith('Facing:')):
                if (line.find('EAST') != -1):
                    player1.facing = Direction.EAST
                    player1.image = Player.east_standing_img
                elif (line.find('NORTH') != -1):
                    player1.facing = Direction.NORTH
                    player1.image = Player.north_standing_img
                elif (line.find('WEST') != -1):
                    player1.facing = Direction.WEST
                    player1.image = Player.west_standing_img
                else:
                    player1.facing = Direction.SOUTH
                    player1.image = Player.south_standing_img
            elif (line.startswith('Number Hearts:')):
                data = int(line[15:(len(line) - 1)]) - 5
                while (data > 0):
                    player1.increase_life_max()
                    data = data - 1
            elif (line.startswith('Missing Health:')):
                data = float(line[16:(len(line) - 1)])
                player1.life.change_health(amount=(-1 * data), defense=1)
            elif (line.startswith('Total Experience:')):
                data = line[18:(len(line) - 1)]
                player1.experience.total_exp = float(data)
            elif (line.startswith('Exp Scale:')):
                data = line[11:(len(line) - 1)]
                player1.experience.exp.scale = float(data)
            elif (line.startswith('Inventory Highlight X:')):
                player1.player_inventory.array[0][0].toggle_highlight()
                data = line[23:(len(line) - 1)]
                player1.player_inventory.highlighted_x = int(data)
            elif (line.startswith('Inventory Highlight Y:')):
                data = line[23:(len(line) - 1)]
                player1.player_inventory.highlighted_y = int(data)
            elif (line.startswith('Visibility Scale:')):
                data = line[18:(len(line) - 1)]
                player1.visibility.scale = float(data)
            elif (line.startswith('Extra Slots:')):
                data = int(line[13:(len(line) - 1)])
                while (data > 0):
                    player1.increase_inventory_max()
                    data = data - 1
            elif (line.startswith('Selected:')):
                data = line[10:(len(line) - 1)]
                if (data == 'True'):
                    player1.player_inventory.array[row][slot].toggle_select()
                    if (player1.player_inventory.array[row][slot].item.type == Type.Weapon):
                        player1.selected_weapon = player1.player_inventory.array[row][slot]
                    elif (player1.player_inventory.array[row][slot].item.type == Type.Helmet):
                        player1.selected_helmet = player1.player_inventory.array[row][slot]
                    elif (player1.player_inventory.array[row][slot].item.type == Type.Chestpiece):
                        player1.selected_chestpiece = player1.player_inventory.array[row][slot]
                    elif (player1.player_inventory.array[row][slot].item.type == Type.Leggings):
                        player1.selected_leggings = player1.player_inventory.array[row][slot]
                    elif (player1.player_inventory.array[row][slot].item.type == Type.Footwear):
                        player1.selected_footwear = player1.player_inventory.array[row][slot]
                    elif (player1.player_inventory.array[row][slot].item.type == Type.Torch):
                        player1.selected_torch = player1.player_inventory.array[row][slot]
            elif (line.startswith('Highlighted:')):
                data = line[13:(len(line) - 1)]
                if (data == 'True'):
                    player1.player_inventory.array[row][slot].toggle_highlight()
                if (slot == 4):
                    slot = 0
                    row = row + 1
                else:
                    slot = slot + 1
            elif (line.startswith('Type:')):
                if (line.find('Weapon') != -1):
                    to_add = pItem(item_enum=Type.Weapon, aX=(player1.player_inventory.array[row][slot].x + 10), aY=(player1.player_inventory.array[row][slot].y + 10), frame=player1.player_inventory.array[row][slot], a_player=player1)
                    player1.player_inventory.array[row][slot].item = to_add
                elif (line.find('Helmet') != -1):
                    to_add = pItem(item_enum=Type.Helmet, aX=(player1.player_inventory.array[row][slot].x + 10), aY=(player1.player_inventory.array[row][slot].y + 10), frame=player1.player_inventory.array[row][slot], a_player=player1)
                    player1.player_inventory.array[row][slot].item = to_add
                elif (line.find('Chestpiece') != -1):
                    to_add = pItem(item_enum=Type.Chestpiece, aX=(player1.player_inventory.array[row][slot].x + 10), aY=(player1.player_inventory.array[row][slot].y + 10), frame=player1.player_inventory.array[row][slot], a_player=player1)
                    player1.player_inventory.array[row][slot].item = to_add
                elif (line.find('Leggings') != -1):
                    to_add = pItem(item_enum=Type.Leggings, aX=(player1.player_inventory.array[row][slot].x + 10), aY=(player1.player_inventory.array[row][slot].y + 10), frame=player1.player_inventory.array[row][slot], a_player=player1)
                    player1.player_inventory.array[row][slot].item = to_add
                elif (line.find('Footwear') != -1):
                    to_add = pItem(item_enum=Type.Footwear, aX=(player1.player_inventory.array[row][slot].x + 10), aY=(player1.player_inventory.array[row][slot].y + 10), frame=player1.player_inventory.array[row][slot], a_player=player1)
                    player1.player_inventory.array[row][slot].item = to_add
                elif (line.find('Torch') != -1):
                    to_add = pItem(item_enum=Type.Torch, aX=(player1.player_inventory.array[row][slot].x + 10), aY=(player1.player_inventory.array[row][slot].y + 10), frame=player1.player_inventory.array[row][slot], a_player=player1)
                    player1.player_inventory.array[row][slot].item = to_add
                else:
                    to_add = pItem(item_enum=Type.Potion, aX=(player1.player_inventory.array[row][slot].x + 10), aY=(player1.player_inventory.array[row][slot].y + 10), frame=player1.player_inventory.array[row][slot], a_player=player1)
                    player1.player_inventory.array[row][slot].item = to_add
            elif (line.startswith('Value:')):
                data = line[7:(len(line) - 1)]
                player1.player_inventory.array[row][slot].item.attack_strength_defense = float(data)
            elif (line.startswith('Durability:')):
                data = line[12:(len(line) - 1)]
                player1.player_inventory.array[row][slot].item.durability = float(data)
                player1.player_inventory.array[row][slot].item.change_cracks()
            elif (line.startswith('Durability Max:')):
                data = line[16:(len(line) - 1)]
                player1.player_inventory.array[row][slot].item.durability_max = float(data)
            elif (line.startswith('Rarity:')):
                data = int(line[8:(len(line) - 1)])
                player1.player_inventory.array[row][slot].item.rarity = data
                if (data == 4):
                    player1.player_inventory.array[row][slot].item.rarity_img.image = Rarity.mythical
                elif (data == 3):
                    player1.player_inventory.array[row][slot].item.rarity_img.image = Rarity.epic
                elif (data == 2):
                    player1.player_inventory.array[row][slot].item.rarity_img.image = Rarity.rare
                elif (data == 1):
                    player1.player_inventory.array[row][slot].item.rarity_img.image = Rarity.uncommon
    with open('saves/map.txt', 'r', encoding = 'utf-8') as f:
        room_num = 0
        is_room = True
        for line in f:
            if (line.startswith('Room Number:')):
                data = line[13:(len(line) - 1)]
                room_num = int(data)
                to_add = Room(direc=None, backgroundX=startX, backgroundY=startY, this_level=0)
                room_map.room_dict[room_num] = to_add
            elif (line.startswith('Direction:')):
                if (line.find('EAST') != -1):
                    room_map.room_dict[room_num].location = Direction.EAST
                elif (line.find('NORTH') != -1):
                    room_map.room_dict[room_num].location = Direction.NORTH
                elif (line.find('WEST') != -1):
                    room_map.room_dict[room_num].location = Direction.WEST
                elif (line.find('SOUTH') != -1):
                    room_map.room_dict[room_num].location = Direction.SOUTH
                elif (line.find('NE') != -1):
                    room_map.room_dict[room_num].location = Direction.NE
                elif (line.find('NW') != -1):
                    room_map.room_dict[room_num].location = Direction.NW
                elif (line.find('SE') != -1):
                    room_map.room_dict[room_num].location = Direction.SE
                else:
                    room_map.room_dict[room_num].location = Direction.SW
            elif (line.startswith('Level:')):
                data = line[7:(len(line) - 1)]
                if (is_room):
                    room_map.room_dict[room_num].level = int(data)
                else:
                    room_num = int(data)
                    room_map.corner_numbers[room_num] = []
            elif (line.startswith('Monster:')):
                room_map.room_dict[room_num].entities.append(Monster(backgroundX=startX, backgroundY=startY, this_room=room_map.room_dict[room_num]))
            elif (line.startswith('Item:')):
                room_map.room_dict[room_num].entities.append(Item(backX=startX, backY=startY, this_room=room_map.room_dict[room_num]))
            elif (line.startswith('Door:')):
                room_map.room_dict[room_num].entities.append(Door(backgroundX=startX, backgroundY=startY, direct=None))
            elif (line.startswith('Monster Type:')):
                data = line[14:(len(line) - 1)]
                room_map.room_dict[room_num].entities[-1].monster_type = data
                if (data == 'Bat'):
                    room_map.room_dict[room_num].entities[-1].standing_img_south = Monster.bat_south_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_south = Monster.bat_south_moving
                    room_map.room_dict[room_num].entities[-1].standing_img_east = Monster.bat_east_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_east = Monster.bat_east_moving
                    room_map.room_dict[room_num].entities[-1].standing_img_north = Monster.bat_north_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_north = Monster.bat_north_moving
                    room_map.room_dict[room_num].entities[-1].standing_img_west = Monster.bat_west_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_west = Monster.bat_west_moving
                    room_map.room_dict[room_num].entities[-1].attacking_img_east = Monster.bat_east_moving
                    room_map.room_dict[room_num].entities[-1].attacking_img_north = Monster.bat_north_moving
                    room_map.room_dict[room_num].entities[-1].attacking_img_south = Monster.bat_south_moving
                    room_map.room_dict[room_num].entities[-1].attacking_img_west = Monster.bat_west_moving
                elif (data == 'Slime'):
                    room_map.room_dict[room_num].entities[-1].standing_img_south = Monster.slime_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_south = Monster.slime_NS_moving
                    room_map.room_dict[room_num].entities[-1].standing_img_east = Monster.slime_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_east = Monster.slime_east_moving
                    room_map.room_dict[room_num].entities[-1].standing_img_north = Monster.slime_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_north = Monster.slime_NS_moving
                    room_map.room_dict[room_num].entities[-1].standing_img_west = Monster.slime_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_west = Monster.slime_west_moving
                    room_map.room_dict[room_num].entities[-1].attacking_img_east = Monster.slime_east_moving
                    room_map.room_dict[room_num].entities[-1].attacking_img_north = Monster.slime_NS_moving
                    room_map.room_dict[room_num].entities[-1].attacking_img_south = Monster.slime_NS_moving
                    room_map.room_dict[room_num].entities[-1].attacking_img_west = Monster.slime_west_moving
                else:
                    room_map.room_dict[room_num].entities[-1].standing_img_south = Monster.skeleton_south_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_south = Monster.skeleton_south_moving
                    room_map.room_dict[room_num].entities[-1].standing_img_east = Monster.skeleton_east_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_east = Monster.skeletont_east_moving
                    room_map.room_dict[room_num].entities[-1].standing_img_north = Monster.skeleton_north_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_north = Monster.skeleton_north_moving
                    room_map.room_dict[room_num].entities[-1].standing_img_west = Monster.skeleton_west_standing
                    room_map.room_dict[room_num].entities[-1].moving_img_west = Monster.skeleton_west_moving
                    room_map.room_dict[room_num].entities[-1].attacking_img_east = Monster.skeletont_east_attack
                    room_map.room_dict[room_num].entities[-1].attacking_img_north = Monster.skeleton_north_attack
                    room_map.room_dict[room_num].entities[-1].attacking_img_south = Monster.skeleton_south_attack
                    room_map.room_dict[room_num].entities[-1].attacking_img_west = Monster.skeleton_west_attack
            elif (line.startswith('Multiplier:')):
                data = line[12:(len(line) - 1)]
                room_map.room_dict[room_num].entities[-1].multiplier = float(data)
            elif (line.startswith('Health:')):
                data = line[8:(len(line) - 1)]
                room_map.room_dict[room_num].entities[-1].health = float(data)
            elif (line.startswith('Speed:')):
                data = line[7:(len(line) - 1)]
                room_map.room_dict[room_num].entities[-1].speed = float(data)
            elif (line.startswith('Attack:')):
                data = line[8:(len(line) - 1)]
                room_map.room_dict[room_num].entities[-1].attack = float(data)
            elif (line.startswith('Sight:')):
                data = line[7:(len(line) - 1)]
                room_map.room_dict[room_num].entities[-1].sight = float(data)
            elif (line.startswith('Is Moving:')):
                data = line[11:(len(line) - 1)]
                if (data == 'True'):
                    room_map.room_dict[room_num].entities[-1].is_moving = True
                else:
                    room_map.room_dict[room_num].entities[-1].is_moving = False
            elif (line.startswith('Facing:')):
                if (line.find('EAST') != -1):
                    room_map.room_dict[room_num].entities[-1].facing = Direction.EAST
                    room_map.room_dict[room_num].entities[-1].image = room_map.room_dict[room_num].entities[-1].standing_img_east
                elif (line.find('NORTH') != -1):
                    room_map.room_dict[room_num].entities[-1].facing = Direction.NORTH
                    room_map.room_dict[room_num].entities[-1].image = room_map.room_dict[room_num].entities[-1].standing_img_north
                elif (line.find('WEST') != -1):
                    room_map.room_dict[room_num].entities[-1].facing = Direction.WEST
                    room_map.room_dict[room_num].entities[-1].image = room_map.room_dict[room_num].entities[-1].standing_img_west
                else:
                    room_map.room_dict[room_num].entities[-1].facing = Direction.SOUTH
                    room_map.room_dict[room_num].entities[-1].image = room_map.room_dict[room_num].entities[-1].standing_img_south
            elif (line.startswith('X:')):
                data = line[3:(len(line) - 1)]
                room_map.room_dict[room_num].entities[-1].x = float(data)
            elif (line.startswith('Y:')):
                data = line[3:(len(line) - 1)]
                room_map.room_dict[room_num].entities[-1].y = float(data)
            elif (line.startswith('Next Coord:')):
                data = line[12:(len(line) - 1)]
                if (data == 'None'):
                    room_map.room_dict[room_num].entities[-1].next_coord = None
                else:
                    room_map.room_dict[room_num].entities[-1].next_coord = float(data)
                    if (room_map.room_dict[room_num].entities[-1].is_moving):
                        if (room_map.room_dict[room_num].entities[-1].facing == Direction.EAST or room_map.room_dict[room_num].entities[-1].facing == Direction.WEST):
                            room_map.room_dict[room_num].entities[-1].x = float(data)
                        else:
                            room_map.room_dict[room_num].entities[-1].y = float(data)
            elif (line.startswith('Item Type:')):
                if (line.find('Weapon') != -1):
                    room_map.room_dict[room_num].entities[-1].item_enum = Type.Weapon
                    room_map.room_dict[room_num].entities[-1].image = Item.sword
                elif (line.find('Helmet') != -1):
                    room_map.room_dict[room_num].entities[-1].item_enum = Type.Helmet
                    room_map.room_dict[room_num].entities[-1].image = Item.helmet
                elif (line.find('Chestpiece') != -1):
                    room_map.room_dict[room_num].entities[-1].item_enum = Type.Chestpiece
                    room_map.room_dict[room_num].entities[-1].image = Item.chestpiece
                elif (line.find('Leggings') != -1):
                    room_map.room_dict[room_num].entities[-1].item_enum = Type.Leggings
                    room_map.room_dict[room_num].entities[-1].image = Item.leggings
                elif (line.find('Footwear') != -1):
                    room_map.room_dict[room_num].entities[-1].item_enum = Type.Footwear
                    room_map.room_dict[room_num].entities[-1].image = Item.hermes
                elif (line.find('Torch') != -1):
                    room_map.room_dict[room_num].entities[-1].item_enum = Type.Torch
                    room_map.room_dict[room_num].entities[-1].image = Item.torch
                else:
                    room_map.room_dict[room_num].entities[-1].item_enum = Type.Potion
                    room_map.room_dict[room_num].entities[-1].image = Item.potion
            elif (line.startswith('Is Gold:')):
                data = line[9:(len(line) - 1)]
                if (data == 'True'):
                    room_map.room_dict[room_num].entities[-1].is_gold = True
                    room_map.room_dict[room_num].entities[-1].image = Door.level_up
                else:
                    room_map.room_dict[room_num].entities[-1].is_gold = False
            elif (line.startswith('Rotation:')):
                data = line[10:(len(line) - 1)]
                room_map.room_dict[room_num].entities[-1].rotation = float(data)
            elif (line.startswith('Corner Dictionary:')):
                is_room = False
                room_num = 0
            elif (line.startswith('Corner:')):
                data = line[8:(len(line) - 1)]
                room_map.corner_numbers[room_num].append(int(data))
    current_room = room_map.change_to_room(number=player1.room_number, level=player1.level)
    displayed_level.update_level(new_level=player1.level)

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
        elif (symbol == key.ESCAPE):
            return pyglet.event.EVENT_HANDLED
    elif current_state == State.Game and player_is_alive:
        if (not player1.is_moving and not player1.scheduled_moving):
            player1.queued_direction = None
            player1.scheduled_moving = True
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
            player1.scheduled_moving = False
            pyglet.clock.unschedule(start_moving_player)
            if (player1.is_moving):
                pyglet.clock.unschedule(moving_bounds_check)
                set_next_box_coords()
                valid = check_player_legal_movement()
                if (valid):
                    pyglet.clock.schedule_interval(wait_until_player_in_box, 1/100.0)
                else:
                    player1.stop_moving()
                    set_player_last_valid()
            game_to_inventory()
        elif symbol == key.W:
            player1.queued_direction = None
            player1.scheduled_moving = False
            player_attack()
        elif (symbol == key.ESCAPE):
            return pyglet.event.EVENT_HANDLED
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
        elif symbol == key.R:
            player1.discard_item()
        elif (symbol == key.ESCAPE):
            save_state()
            inventory_to_menu()
            return pyglet.event.EVENT_HANDLED
    elif not player_is_alive:
        if symbol == key.W:
            inventory_to_menu()
        elif (symbol == key.ESCAPE):
            return pyglet.event.EVENT_HANDLED        
            
@window.event
def on_key_release(symbol, modifiers):
    if (current_state == State.Game and player_is_alive):
        if ((symbol == key.UP and player1.facing == Direction.NORTH) or (symbol == key.RIGHT and player1.facing == Direction.EAST) or (symbol == key.DOWN and player1.facing == Direction.SOUTH) or (symbol == key.LEFT and player1.facing == Direction.WEST)):
            player1.scheduled_moving = False
            pyglet.clock.unschedule(start_moving_player)
            if (player1.is_moving):
                pyglet.clock.unschedule(moving_bounds_check)
                set_next_box_coords()
                valid = check_player_legal_movement()
                if (valid):
                    pyglet.clock.schedule_interval(wait_until_player_in_box, 1/100.0)
                else:
                    player1.stop_moving()
                    set_player_last_valid()
        if ((symbol == key.UP and player1.queued_direction == Direction.NORTH) or (symbol == key.RIGHT and player1.queued_direction == Direction.EAST) or (symbol == key.DOWN and player1.queued_direction == Direction.SOUTH) or (symbol == key.LEFT and player1.queued_direction == Direction.WEST)):
            player1.queued_direction = None

if __name__ == '__main__':
    main()