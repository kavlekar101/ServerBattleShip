import socket
import threading
import BattleShip
import pickle

# the header in the protocols, that means that this is the envelope part of the message
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# AF_INET is over the internet (which specifies what we are looking for), and the method to send it is SOCK_STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

players = []


'''
    receives information from the client(s)
'''
def receive(conn):
    # blocking line of code because we won't proceed until we receive something
    msgLength = conn.recv(HEADER).decode(FORMAT)

    msg = ""

    if msgLength:
        msgLength = int(msgLength)

        try:
            msg = int(conn.recv(msgLength).decode(FORMAT))
        except ValueError as v:
            msg = conn.recv(msgLength).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

    return msg


'''
    This handles the clients, taking care of client to client data transfers and 
    making sure that the game states are up to date
'''
def handleClient(conn, addr):
    global turn
    print(f"[NEW CONNECTION] {addr} connected.")

    # This is where we will initialize the game on the server side

    # this holds index of the ship associated with the client. This works 
    # because the first active thread is the server, so subtract one, then 
    # the second active would be the first client and the third would be 
    # the second client. To get the index, just do - 1 - 1 or -2
    index = 0 if threading.currentThread().getName() == "Player1" else 1
    
    # this is the protocol for sending ships over the sockets.
    players.append(BattleShip.BattleShip(500, (127, 127, 127)))
    numShips = 5
    for i in range(numShips):
        msgLength = conn.recv(HEADER).decode(FORMAT)
        msgLength = int(msgLength)
        msg = conn.recv(msgLength).decode(FORMAT)
        currShip = []

        # we know that this will always be a multiple of 3, so it is fine to do
        for j in range(int(msgLength / 3)):
            x = int(msg[3 * j])
            y = int(msg[3 * j + 1])
            hit = int(msg[3 * j + 2])
            currShip.append((x, y, hit))
        players[index].ships.append(currShip)

    # the protocol for this game is here
    while connected:


        # handles which thread needs to go
        if threading.currentThread().getName() == "Player1":
            while turn % 2 != 0:
                num = 1
        elif threading.currentThread().getName() == "Player2":
            while turn % 2 == 0:
                num = 1
        # the client will send the x and y coordinates first, then we will 
        # send back a 'hit' or 'miss' and the coordinates
        x = receive(conn)
        y = receive(conn)

        # sends to the current player whether or not the play was a hit or miss
        row, col = players[abs(index - 1)].didHit(x, y, 0)
        if row != -1 and col != -1:
            msg = "hit"
            conn.send(msg.encode())
            players[abs(index - 1)].ships[row][col] = (x, y, 1)
        else:
            msg = "miss"
            conn.send(msg.encode())

        print(f"[{addr}] {msg}")

        conn.send(str(row).encode())
        conn.send(str(col).encode())

        # this dumps the most current version of both ships to a file so that the clients can read it
        outfile1 = open("Player1", 'wb')
        pickle.dump(players[0].ships, outfile1)
        outfile1.close()

        outfile2 = open("Player2", 'wb')
        pickle.dump(players[1].ships, outfile2)
        outfile2.close()

        turn += 1
        
    
    conn.close()


'''
    Starts the server
'''
def start():
    global turn
    turn = 0

    global connected
    connected = True

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    playerNum = 1
    while playerNum < 3:
        conn, addr = server.accept()
        thread = threading.Thread(name="Player"+str(playerNum),target=handleClient, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS {threading.activeCount() - 1}]")
        playerNum += 1
    

print("[STARTING] server is starting...")
start()
