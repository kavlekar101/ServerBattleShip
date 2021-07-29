import socket
import pygame
import BattleShip
import pickle
import time


HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


'''
    Sends a message to the server
'''
def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)

'''
    Sends an array to the server
'''
def sendArr(arr):
    # Basically, we have a formatted ship order, so we can send the points for each ship, all we need to do is 
    # concatenate the tuples into strings and then send them with the other method

    stringShip = ""
    for x, y, hit in arr:
        stringShip += str(x) + str(y) + str(hit)
    
    send(stringShip)


'''
    Draws the entire GUI which contains the ships, 
    the lines for the battlefield, and the background color
'''

def drawWin(screen):
    screen.fill((0, 0, 255))

    player.drawMisses(screen)

    player.drawHits(screen)

    player.drawShips(screen)

    for i in range(20):
        pygame.draw.line(screen, (0, 0, 0),
                         (50 + i*50, 0), (50 + i*50, 500))

        if i == 9:
            pygame.draw.line(screen, (0, 0, 0),
                             (50 + i*50, 0), (50 + i*50, 500), 5)
        if i < 10:
            pygame.draw.line(screen, (0, 0, 0),
                             (0, 50 + i*50), (1000, 50 + i*50))

'''
    Takes care of the user input, and advances the game
'''
def main():
    global player
    running = True
    pygame.init()
    size = 1000, 500

    screen = pygame.display.set_mode(size)

    player = BattleShip.BattleShip(500, (127, 127, 127))
    player.generateShips()
    player.formatShips()

    for arr in player.ships:
        sendArr(arr)

    # game logic
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = int(pos[0] / 50), int(pos[1] / 50)

                send(str(x))
                send(str(y))

                outcome = client.recv(1024).decode(FORMAT)

                # whether or not the current play was a hit or miss
                row,col = int(client.recv(64).decode(FORMAT)), int(client.recv(64).decode(FORMAT))
                if outcome == "hit":
                    player.hits.append((x,y))
                else:
                    player.misses.append((x,y))

                time.sleep(5)

                # reads the current updated version of the ships from the file
                infile1 = open("Player1", 'rb')
                newShips1 = pickle.load(infile1)
                infile1.close()

                infile2 = open("Player2", 'rb')
                newShips2 = pickle.load(infile2)
                infile2.close()

                # logic for updating the players ships
                try:
                    point = newShips1[row][col]
                    ship = player.ships[row][col]
                    if point[0] == ship[0] and point[1] == ship[1]:
                        player.ships = newShips1
                    else:
                        raise IndexError
                except IndexError as i:
                    point = newShips2[row][col]
                    ship = player.ships[row][col]
                    if point[0] == ship[0] and point[1] == ship[1]:
                        player.ships = newShips2


        drawWin(screen)

        pygame.display.update()

main()
