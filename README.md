# ServerBattleShip
Server based battleship game

This is a server based approach to the well known battleship game.

The modules socket, pygame, pickle, and threading were used.
The custom module called BattleShip was used to represent the game state
The clients initialize a version of battleship in their windows and communicate their ship positions to the server.
The client then alternate turns by telling the server where their player went.
The server then updates the stored ships and sends them to the clients by pickling them.
The clients then unpickle the files and update their battleships.
