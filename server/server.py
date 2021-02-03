

import socket
import threading 
import time 

gameState=False

joueursListe=[[] for k in range(2)]
id = [[k,0] for k in range(4)]
adresselist= [[] for k in range(2)]

def decode (b : bytes):
    s =b.decode("utf-8")
    parts = s.split(',')
    rep= [int(float(part)) for part in parts]
    return rep

def encode (L: list):
    rep=""
    for k in range(len(L)):
        rep+=";"
        for i in range(len(L[k])):
            rep+=str(L[k][i])
            rep+=","

        rep = rep.strip(",")
    rep = rep.strip(";")

    return rep.encode("utf-8")


class test(threading.Thread):
    def __init__(self, connection,adresse):

        threading.Thread.__init__(self)
        self.connection= connection
        self.adresse = adresse    

    def run(self):
        while(1):
            x=self.connection.recv(1024)
            if x != b'':
                print(f"received : {x} from client {self.adresse}")
                self.connection.sendall(b'4')



class connectionGame(threading.Thread):
    def __init__(self, connection,adresse):

        threading.Thread.__init__(self)
        self.connection= connection
        self.adresse = adresse    

    def run(self):
        global gameState
        global adresselist
        global joueursListe

        for k in range(len(id)):
                
                if k==1:
                    gameState=True
                    if id[k][1]==0:
                        id[k][1]=1
                        time.sleep(1/100)
                        self.connection.sendto(str(id[k][0]).encode("utf-8"),self.adresse)
                        adresselist[id[k][0]]=[self.connection,self.adresse]
                        for k in adresselist:
                            k[0].sendto(b'start',k[1])
                        
                        break
                        
                elif id[k][1]==0:
                    id[k][1]=1
                    time.sleep(1/100)
                    self.connection.sendto(str(id[k][0]).encode("utf-8"),self.adresse)
                    adresselist[id[k][0]]=[self.connection,self.adresse]
                        
                    break


        while True:

            while gameState== True:

                data = self.connection.recv(1024)
                if data != b'':

                    data=decode(data)

                    joueursListe[data[0]]=data
                    print(joueursListe)
                    print(encode(joueursListe))
                    time.sleep(1/100)
                    self.connection.send(encode(joueursListe))

                # nbPlayerAlive = 0
                # for k in joueursListe:

                #     if k[-1]==0:
                #         nbPlayerAlive+=1

                # print("nombre de joueurs vivant = "+str(nbPlayerAlive))

                # if nbPlayerAlive ==2 : 
                #     print("Finitéééééééééé")
                #     winner=5
                #     gameState=False
                #     for k in joueursListe:
                #         if k[-1]==1:
                #             winner=k[0]
                #             break

                #     print("THE WINNER IS : "+str(winner))  
                #     break  
                
                    


HOST = '172.21.72.162'  # Standard loopback interface address (localhost)
PORT = 4444   # Port to listen on (non-privileged ports are > 1023)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
while 1:
    s.listen()
    conn, addr = s.accept()

    new_client=connectionGame(conn,addr)
    new_client.start()