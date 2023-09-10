import socket
import random
import pickle
from _thread import *
from game import Game
import asyncio

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "192.168.1.59"
port = 6666
try:
    sock.bind((server, port))
except socket.error as e:
    str(e)

sock.listen(2)  
print("server running. Waiting for connections...")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    p=str(p)
    conn.send(p.encode())

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


def create():
    y = [random.choice('roygbp') for _ in range(4)]
    check="".join(y)
    print(y)
    secret_code = str(check)
    print(secret_code)
    return secret_code


while True:
    conn, addr = sock.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
        secret_code=create()
        secret_code = str(secret_code)
        conn.send(secret_code.encode())
        print("player 1 sent")
    else:
        games[gameId].ready = True
        p = 1
        conn.send(secret_code.encode())
        print("player 2 sent")
    



    start_new_thread(threaded_client, (conn, p, gameId))

# client1_socket, client1_address = sock.accept()
# print("Connection established with client 1", client1_address)

# client2_socket, client2_address= sock.accept()
# print("Connection established with client 2:", client2_address)

# y = [random.choice('roygbp') for _ in range(4)]
# check="".join(y)
# print(y)
# secret_code = str(y)
# print(secret_code)
# client1_socket.send(secret_code.encode())
# print("code sent to client 1")
# client2_socket.send(secret_code.encode())
# print("code sent to client 2")

# flag=0

# def compare(data):
#     print("2")
#     matching_letters = 0
#     for char1, char2 in zip(data, check):
#         if char1 == char2:
#             matching_letters += 1
#     print("3")
#     return matching_letters

# matching_letters2=0

# while True :
#     data1 = client1_socket.recv(1024) 
#     data1 = data1.decode()
#     print(data1)
#     print("1")
#     data2 = client2_socket.recv(1024) 
#     data2 = data2.decode()
#     matching_letters1=compare(data1)
#     print(matching_letters1)
#     match1=str(matching_letters1)
#     client1_socket.send(match1.encode())
#     print("4")
#     matching_letters2=compare(data2)
#     match2=str(matching_letters2)
#     client1_socket.send(match2.encode())
#     if matching_letters1==4 and matching_letters2==4:
#         flag=2
#     if matching_letters1==4:
#         print("4.1")
#         flag=1
#     print("4.2")
#     # if flag==1 :
#     print("5")
#     flg=str(flag)
#     client1_socket.send(flg.encode())
#     client2_socket.send(flg.encode())
#     if flag==1 or flag==2:
#         break
        
    


# client1_socket.close()
# # client2_socket.close()
# sock.close()
