import os
import sys


from p5 import *

import socket
import threading

players = []
step = 5
width = 600
height = 600

NUM_PLAYERS = 2
INDEX = 0

IP = '172.21.72.162'
PORT = 5555

index = 1
all_colors = [Color(255, 0, 0),Color(0, 255, 0),Color(255, 255, 0),Color(0, 255, 255)]
starting_points = [[width/(4*step), height/(4*step)], 
                    [width/(4*step), 3*height/(4*step)], 
                    [3*width/(4*step), height/(4*step)], 
                    [3*width/(4*step), 3*height/(4*step)]]
starting_dirs = [1, 2, 3, 4]

SCENARIO = 0

def decode(by: bytes):
    s = by.decode("utf-8")
    alls = [[int(float(el)) for el in pal.split(',')] for pal in s.split(";")]
    return alls

def encode(l: list):
    s = ""
    for i in range(len(l)):
        s += str(l[i]) + ','
    return s.strip(',').encode('utf-8')


class bike:
    def __init__(self, ide, x, y, d, c):
        self.id = ide
        self.x = x
        self.y = y
        self.d = d
        self.s = 1
        self.c = c
        self.history = []

    def is_dead(self, all_players):
        if self.x < 0 or self.x*step >= width or self.y < 0 or self.y*step >= height:
            self.s = 0
            self.show_all(all_players)
            return True

        for player in all_players:
            for i in range(len(player.history)):
                if player.history[i] == [self.x, self.y] and not (i > len(player.history) - 2 and player.id == self.id):
                    self.s = 0
                    self.show_all(all_players)
                    return True
        return False

    def show(self):
        fill(self.c)
        rect(self.x*step,self.y*step, step,step)

    def show_all(self, all_players):
        background(0)
        for p in all_players:
            if p.s == 1:
                for hist in p.history:
                    fill(p.c)
                    rect(hist[0]*step,hist[1]*step, step,step)


    def update(self):
        self.history.append([self.x, self.y])
        if self.d == 1:
            self.x += 1
        elif self.d == 2:
            self.y -= 1
        elif self.d == 3:
            self.x -= 1
        elif self.d == 4:
            self.y += 1

    def __str__(self):
        return f"{self.id} {self.x} {self.y}"

def setup():
    size(width, height)
    no_stroke()
    background(0)

def draw():
    global INDEX
    if SCENARIO == 0:
        background(0)
        for p in players:
            p.show()

    if SCENARIO == 1:
        players[INDEX].is_dead(players)
        for p in players:
            if p.s == 1:
                p.show()
                p.update()

def key_pressed(event):
    if key == 'UP' and players[INDEX].d != 4:
        players[INDEX].d = 2
    elif key == 'LEFT' and players[INDEX].d != 1:
        players[INDEX].d = 3
    elif key == 'DOWN' and players[INDEX].d != 2:
        players[INDEX].d = 4  
    elif key == 'RIGHT' and players[INDEX].d != 3:
        players[INDEX].d = 1


def update_players(data: list):
    global players
    if len(data) == NUM_PLAYERS and data[NUM_PLAYERS-1] != []:
        for i in range(NUM_PLAYERS):
            if i != INDEX:
                players[i].x = data[i][1]
                players[i].y = data[i][2]
                players[i].d = data[i][3]
                if players[i].s != data[i][-1]:
                    print("dead")
                    players[i].show_all(players)
                players[i].s = data[i][4]



class listener(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        global SCENARIO
        global players
        global INDEX
        players = [bike(index, starting_points[index][0], starting_points[index][1], starting_dirs[index], all_colors[index]) for index in range(NUM_PLAYERS)]
        INDEX = int(s.recv(32).decode("utf-8"))
        print(INDEX)
        while 1:
            start = s.recv(1024)
            print(start.decode("utf-8"))
            if start.decode("utf-8") == "start":
                SCENARIO = 1
                print("""

                    Starting !

                """)
                self.socket.send(encode([players[INDEX].id, players[INDEX].x, players[INDEX].y, players[INDEX].d, players[INDEX].s]))
                while 1:
                    data = s.recv(1024)
                    if data != b"":
                        update_players(decode(data))
                        time.sleep(1/(120*NUM_PLAYERS))
                        self.socket.send(encode([players[INDEX].id, players[INDEX].x, players[INDEX].y, players[INDEX].d, players[INDEX].s]))
                        



if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    lis = listener(s)
    lis.start()
    run(frame_rate=30)

