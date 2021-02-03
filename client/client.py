import os
import sys
import socket
import threading
from p5 import *

IP = '0.0.0.0'
PORT = 4444
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

STEP = 5
WIDTH = 600
HEIGHT = 600
INDEX = 0 #Id of this client
COLORS = [Color(255, 0, 0),Color(0, 255, 0), Color(255, 255, 0), Color(0, 255, 255)]

players = []
this_player = None
scenario = 0
clear = 0


def decode_all(by: bytes) -> list:
    return [[int(float(el)) for el in pal.split(',')] for pal in by.decode("utf-8").split(";")]

def decode_one(by: bytes) -> list:
    return [int(float(el)) for el in by.decode("utf-8").split(",")]

def encode(l: list) -> bytes:
    s = ""
    for i in range(len(l)):
        s += str(l[i]) + ','
    return s.strip(',').encode('utf-8')


class bike:
    def __init__(self, index, x, y, d, s, c):
        self.id = index
        self.x = x
        self.y = y
        self.d = d
        self.s = 1
        self.c = c
        self.history = []

    def show(self) -> None:
        fill(self.c)
        rect(self.x*STEP,self.y*STEP, STEP,STEP)

    def update(self, data: list) -> bool:
        global clear
        global players
        self.x = data[1]
        self.y = data[2]
        self.d = data[3]
        self.history.append([self.x, self.y])
        if self.s != data[-1]:
            print(f"Player {self.id} is dead")
            self.history = []
            self.s = 0
            clear = 1
        self.s = data[4]
                

    def __str__(self):
        return f"{self.id} x:{self.x} y:{self.y} state:{self.s} dir:{self.d}"

    def __repr__(self):
        return f"{self.id} x:{self.x} y:{self.y} state:{self.s} dir:{self.d}"

def setup():
    size(WIDTH, HEIGHT)
    no_stroke()
    background(0)
    lis.start()

def draw():
    global INDEX
    global STEP
    global players
    global scenario
    global clear
    global this_player

    if scenario == 0:
        background(0)

    if scenario == 17:
        background(0)
        this_player.show()

    if scenario == 1:
        if clear == 1:
            print("CLEAR")
            background(0)
            for player in players:
                if player.s == 1:
                    for hist in player.history:
                        fill(player.c)
                        rect(hist[0]*STEP, hist[1]*STEP, STEP, STEP)
            clear = 0

        for player in players:
            if player.s == 1:
                player.show()

        


def key_pressed(event):
    if scenario == 1:
        dir = 0
        if key == 'UP' and players[INDEX].d != 4:
            dir = 2
        elif key == 'LEFT' and players[INDEX].d != 1:
            dir = 3
        elif key == 'DOWN' and players[INDEX].d != 2:
            dir = 4  
        elif key == 'RIGHT' and players[INDEX].d != 3:
            dir = 1
        if dir != 0:
            SERVER.send(str(dir).encode("utf-8"))
    
    if key == "q":
        exit()
    


class listener(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        global scenario
        global players
        global INDEX
        global this_player
        player = decode_one(self.socket.recv(1024))
        this_player = bike(player[0],player[1],player[2],player[3], player[4], COLORS[player[0]])
        INDEX = player[0]
        scenario = 17

        while 1:
            start = self.socket.recv(1024)
            print(start.decode("utf-8"))
            if start.decode("utf-8") == "start":
                scenario = 1
                print("""

                                Starting !

                """)
                data = self.socket.recv(1024)
                if data != b"":
                    players = [bike(player_data[0],
                                    player_data[1],
                                    player_data[2],
                                    player_data[3], 
                                    player_data[4], 
                                    COLORS[player_data[0]]) 
                                for player_data in decode_all(data)
                                ]
                while 1:
                    data = self.socket.recv(1024)
                    if data != b"":
                        data = decode_all(data)
                        for i,player in enumerate(players):
                            player.update(data[i])
                        



if __name__ == "__main__":
    SERVER.connect((IP, PORT))
    lis = listener(SERVER)
    run(frame_rate=30)

