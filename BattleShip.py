import pygame
import random


class BattleShip:
    # anything declared up here is set for ALL instances
    CELL_SIZE = 50

    def __init__(self, OFFSET, color, visible=True):
        self.OFFSET = OFFSET
        self.color = color
        self.visible = visible
        self.deadShips = 0
        self.ships = []
        self.setShips = [0, 0, 1, 2, 1, 1]
        self.shipOrder = []
        self.misses = []
        self.hits = []

    '''
        Generates all of the battleships in a random position on the board.
    '''
    def generateShips(self):

        while sum(self.setShips) != 0:
            dir = random.randint(1, 4)

            shipSize = random.randint(2, 5)
            while self.setShips[shipSize] == 0:
                shipSize = random.randint(2, 5)

            # there is only a certain range which can contain the ship
            twoShipPoint = random.randint(0, 9)

            # if the dir number is 1 then the ship is going up
            # if the dir number is 2 then the ship is going down
            # if the dir number is 3 then the ship is going left
            # if the dir number is 4 then the ship is going right
            points = []
            if dir == 1 or dir == 3:
                oneShipPoint = random.randint(-1 + shipSize, 9)

                # generates the points for the ships and checks that 
                # these points do not already exist
                index = 0
                while index < shipSize:
                    if index != 0:
                        oneShipPoint -= 1
                    if dir == 1:
                        points.append((twoShipPoint, oneShipPoint, 0))

                        index += 1
                        # checks if there is already this points, which means we need to restart
                        while self.ships.count((twoShipPoint, oneShipPoint, 0)) == 1:
                            oneShipPoint = random.randint(-1 + shipSize, 9)
                            twoShipPoint = random.randint(0, 9)
                            points.clear()
                            index = 0
                    else:
                        points.append((oneShipPoint, twoShipPoint, 0))

                        index += 1
                        # checks if there is already this points, which means we need to restart
                        while self.ships.count((oneShipPoint, twoShipPoint, 0)) == 1:
                            oneShipPoint = random.randint(-1 + shipSize, 9)
                            twoShipPoint = random.randint(0, 9)
                            points.clear()
                            index = 0

            else:
                oneShipPoint = random.randint(0, 10 - shipSize)

                # generates the points for the ships and checks that
                # these points do not already exist
                index = 0
                while index < shipSize:
                    if index != 0:
                        oneShipPoint += 1
                    if dir == 2:
                        points.append((twoShipPoint, oneShipPoint, 0))

                        index += 1
                        # checks if there is already this points, which means we need to restart
                        while self.ships.count((twoShipPoint, oneShipPoint, 0)) == 1:
                            oneShipPoint = random.randint(0, 10 - shipSize)
                            twoShipPoint = random.randint(0, 9)
                            points.clear()
                            index = 0
                    else:
                        points.append((oneShipPoint, twoShipPoint, 0))

                        index += 1
                        # checks if there is already this points, which means we need to restart
                        while self.ships.count((oneShipPoint, twoShipPoint, 0)) == 1:
                            oneShipPoint = random.randint(0, 10 - shipSize)
                            twoShipPoint = random.randint(0, 9)
                            points.clear()
                            index = 0

            self.setShips[shipSize] -= 1
            self.shipOrder.append(shipSize)
            self.ships.extend(points)

    '''
        Changes the format of the ships array from 1D to 2D,
        It becomes an array of ships and each ship is an array of points and whether it has been hit or not
    '''
    def formatShips(self):
        newShips = []
        for num in self.shipOrder:
            currShip = []
            for i in range(num):
                currShip.append(self.ships.pop(0))
            newShips.append(currShip)
        self.ships = newShips

    '''
        Draws the opponents ships and the players ships.
    '''
    def drawShips(self, screen):
        for arr in self.ships:
            for x, y, count in arr:
                if self.visible:
                    pygame.draw.rect(screen, self.color, pygame.Rect(
                        x * 50 + self.OFFSET, y * 50, self.CELL_SIZE, self.CELL_SIZE))
                if count == 1:
                    pygame.draw.circle(screen, (255, 0, 0),
                                    (x * 50 + self.OFFSET + 25, y * 50 + 25), 10)
    
    '''
        Draws the misses.
    '''

    def drawMisses(self, screen):
        for x, y in self.misses:
            pygame.draw.circle(screen, (255, 255, 255),
                               (x * 50 + abs(self.OFFSET - 500) + 25, y * 50 + 25), 10)

    '''
        Sees if the current play was a hit or miss
    '''
    def didHit(self, x, y, offset):
        for arr in self.ships:
            if arr.count((x, y, 0)) == 1:
                return self.ships.index(arr), arr.index((x - offset, y, 0))
        return -1, -1

    '''
        Draws the hits on the oppenents
    '''
    def drawHits(self, screen):
        for x, y in self.hits:
            pygame.draw.circle(screen, (255, 0, 0),
                            (x * 50 + abs(self.OFFSET - 500) + 25, y * 50 + 25), 10)