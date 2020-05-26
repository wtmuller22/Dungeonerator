import socket
from _thread import *
import pickle, pyglet
from game.a_game import Game
from game.player import Player
from game.visibility import Visibility
from game.cardinal_direction import Direction

connected = set()
curr_game = None
idCount = 0

def start_server():
    server = "192.168.1.74"
    port = 5555
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)
    
    s.listen()
    print("Waiting for a connection, Server Started")
    
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
    
        if idCount == 0:
            curr_game = Game()
            print("Creating a new game...")

        start_new_thread(threaded_client, (conn, idCount))
        idCount += 1


def threaded_client(conn, p):
    global idCount
    conn.send(str.encode(str(p)))
    
    player = Player(a_scale=1, given_name=('player' + str(p)), backgroundX=0, backgroundY=0, darkness=Visibility(a_scale=1))
    curr_game.players.append(player)

    while True:
        try:
            data = conn.recv(4096).decode()

            if not data:
                break
            else:
                if data == "MoveUp":
                    curr_game.players[p].queued_direction = None
                    curr_game.players[p].scheduled_moving = True
                    curr_game.players[p].change_direction(Direction.NORTH)
                    pyglet.clock.schedule_once(curr_game.start_moving_player, 0.10, p)
                elif data == "MoveRight":
                    curr_game.players[p].queued_direction = None
                    curr_game.players[p].scheduled_moving = True
                    curr_game.players[p].change_direction(Direction.EAST)
                    pyglet.clock.schedule_once(curr_game.start_moving_player, 0.10, p)
                elif data == "MoveDown":
                    curr_game.players[p].queued_direction = None
                    curr_game.players[p].scheduled_moving = True
                    curr_game.players[p].change_direction(Direction.SOUTH)
                    pyglet.clock.schedule_once(curr_game.start_moving_player, 0.10, p)
                elif data == "MoveLeft":
                    curr_game.players[p].queued_direction = None
                    curr_game.players[p].scheduled_moving = True
                    curr_game.players[p].change_direction(Direction.WEST)
                    pyglet.clock.schedule_once(curr_game.start_moving_player, 0.10, p)
                elif data == "QueueUp":
                    curr_game.players[p].queued_direction = Direction.NORTH
                elif data == "QueueRight":
                    curr_game.players[p].queued_direction = Direction.NORTH
                elif data == "QueueLeft":
                    curr_game.players[p].queued_direction = Direction.NORTH
                elif data == "QueueDown":
                    curr_game.players[p].queued_direction = Direction.NORTH
                elif data == "InvenValid":
                    curr_game.players[p].queued_direction = None
                    curr_game.players[p].scheduled_moving = False
                    pyglet.clock.unschedule(curr_game.start_moving_player)
                    pyglet.clock.unschedule(curr_game.moving_bounds_check)
                    curr_game.set_next_box_coords(p)
                    pyglet.clock.schedule_interval(curr_game.wait_until_player_in_box, 1/100.0, p)
                elif data == "InvenNot":
                    curr_game.players[p].queued_direction = None
                    curr_game.players[p].scheduled_moving = False
                    pyglet.clock.unschedule(curr_game.start_moving_player)
                    pyglet.clock.unschedule(curr_game.moving_bounds_check)
                    curr_game.set_next_box_coords(p)
                    curr_game.players[p].stop_moving()
                    curr_game.set_player_last_valid(p)
                elif data == "Inven":
                    curr_game.players[p].queued_direction = None
                    curr_game.players[p].scheduled_moving = False
                    pyglet.clock.unschedule(curr_game.start_moving_player)
                elif data == "Attack":
                    curr_game.players[p].queued_direction = None
                    curr_game.players[p].scheduled_moving = False
                    curr_game.player_attack(p)
                elif data == "InvenUp":
                    curr_game.players[p].change_highlight(direc=Direction.NORTH)
                elif data == "InvenRight":
                    curr_game.players[p].change_highlight(direc=Direction.EAST)
                elif data == "InvenDown":
                    curr_game.players[p].change_highlight(direc=Direction.SOUTH)
                elif data == "InvenLeft":
                    curr_game.players[p].change_highlight(direc=Direction.WEST)
                elif data == "Toggle":
                    curr_game.players[p].toggle_select_highlight()
                elif data == "Discard":
                    curr_game.players[p].discard_item()
                elif data == "Quit":
                    break
                elif data == "ReleaseValid":
                    curr_game.players[p].scheduled_moving = False
                    pyglet.clock.unschedule(curr_game.start_moving_player)
                    pyglet.clock.unschedule(curr_game.moving_bounds_check)
                    curr_game.set_next_box_coords(p)
                    pyglet.clock.schedule_interval(curr_game.wait_until_player_in_box, 1/100.0, p)
                elif data == "ReleaseNot":
                    curr_game.players[p].scheduled_moving = False
                    pyglet.clock.unschedule(curr_game.start_moving_player)
                    pyglet.clock.unschedule(curr_game.moving_bounds_check)
                    curr_game.set_next_box_coords(p)
                    curr_game.players[p].stop_moving()
                    curr_game.set_player_last_valid(p)
                elif data == "Release":
                    curr_game.players[p].scheduled_moving = False
                    pyglet.clock.unschedule(curr_game.start_moving_player)
                elif data == "Dequeue":
                    curr_game.players[p].queued_direction = None

                conn.sendall(pickle.dumps(curr_game))
        except:
            break

    print("Lost connection")
    try:
        if p != 0:
            curr_game.players[p] = None
            print("Removing Player", p)
        else:
            conn.close()
            print("Closing Server")
    except:
        pass
