import socket
import threading 
import time 
from p5 import Color

HOST = '0.0.0.0'  
PORT = 4444   
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

NUM_PLAYERS = 4
WIDTH = 600 #Screen width
HEIGHT = 600 #Screen height
FPS = 10
STEP = 5
STARTS_POS = [[  WIDTH/(4*STEP),   HEIGHT/(4*STEP)], 
              [  WIDTH/(4*STEP), 3*HEIGHT/(4*STEP)], 
              [3*WIDTH/(4*STEP),   HEIGHT/(4*STEP)], 
              [3*WIDTH/(4*STEP), 3*HEIGHT/(4*STEP)]]
COLOR_NAMES = ["RED", "GREEN", "YELLOW", "CYAN"]
STARTS_DIR = [1, 2, 4, 3]

history = [[] for i in range(NUM_PLAYERS)]
players = []
addresses = []
started = False


def decode_one(b : bytes) -> list:
    return [int(float(part)) for part in b.decode("utf-8").split(',')]


def encode_all(L: list) -> bytes:
    rep = ""
    for k in range(len(L)):
        rep += ";"
        for i in range(len(L[k])):
            rep += str(L[k][i])
            rep += ","
        rep = rep.strip(",")
    rep = rep.strip(";")
    return rep.encode("utf-8")


def encode_one(l: list) -> bytes:
    s = ""
    for i in range(len(l)):
        s += str(l[i]) + ','
    return s.strip(',').encode('utf-8')


class update(threading.Thread):
    def __init__(self, fr):
        threading.Thread.__init__(self)
        self.fr = fr
    
    def run(self):
        global players
        global addresses
        global SERVER
        time.sleep(1)
        while 1:
            start_time = time.time()
            count = 0
            for i,player in enumerate(players):
                if player[4] == 1:
                    count += 1
                    # Update history
                    history[i].append([player[1], player[2]])
                    # Update position
                    if player[3] == 1:
                        player[1] += 1
                    elif player[3] == 2:
                        player[2] -= 1
                    elif player[3] == 3:
                        player[1] -= 1
                    elif player[3] == 4:
                        player[2] += 1

                    #Check if dead
                    if player[1] < 0 or player[1]*STEP >= WIDTH or player[2] < 0 or player[2]*STEP >= HEIGHT:
                        player[4] = 0

                    for j, other in enumerate(players):
                        if other[4] == 1:
                            for pos in history[j]:
                                if [player[1], player[2]] == pos:
                                    player[4] = 0

            if count <= 1:
                for i,player in enumerate(players):
                    if player[-1] == 1:
                        print(f"AND THE WINNER IS {COLOR_NAMES[i]} !!!!!!!!")
                SERVER.close()
                break

            for address in addresses:
                address[0].sendto(encode_all(players), address[1])

            end_time = time.time()
            sleep_time = 1/self.fr - (end_time - start_time) if 1/self.fr > (end_time - start_time) else 0.01
            time.sleep(sleep_time)
            # time.sleep(1)


class connectionGame(threading.Thread):
    def __init__(self, connection, address):

        threading.Thread.__init__(self)
        self.connection= connection
        self.address = address    

    def run(self):
        global started
        global addresses
        global players
        global STARTS_DIR
        global STARTS_POS
        global NUM_PLAYERS
        
        self.index = len(players)
        player = [self.index, STARTS_POS[self.index][0], STARTS_POS[self.index][1], STARTS_DIR[self.index], 1]
        players.append(player)
        print(player)

        self.connection.sendto(encode_one(player), self.address)

        addresses.append([self.connection, self.address])

        if len(players) == NUM_PLAYERS:
            time.sleep(1)
            for address in addresses:
                address[0].sendto(b'start', address[1])
                started = True
            upd = update(FPS)
            upd.start()
            print(f"Game started with {NUM_PLAYERS} players")
        else:
            print(f"Waiting for {NUM_PLAYERS-len(players)} players")

        while True:
            if started:
                new_dir = self.connection.recv(32)
                if new_dir != b'':
                    players[self.index][3] = int(float(new_dir.decode("utf-8")))
            else:
                time.sleep(1/10)
                


SERVER.bind((HOST, PORT))

while 1:
    SERVER.listen()
    conn, addr = SERVER.accept()

    new_client = connectionGame(conn,addr)
    new_client.start()