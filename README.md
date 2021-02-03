# Light Cycle

Made by Adem RAHAL & Thomas JULDO 

## Installation
- `make install` to install p5
- `make glfw` to install GLFW if necessary

## The Server

### Description
The server hosts the clients, wait for the players to connect, sync their start and update their positions based on their direction given by the listener class. It then send to the clients their current informations every at `FPS` (by default 10) fps. It checks if the game has not ended (more than one player left), and otherwise stops the game.

### Initialisation
Set the host ip in `HOST` and the host port in `PORT`, as well as the number of players in `NUM_PLAYERS`.

### Launch
To launch the server simply use `make server`.

## The Client

### Description
The client only displays the state of the game and send the direction the player wants to go toward. It clears dead players without impacting the game. Move using the keypad arrows and exit by pressing `q`.

### Initialisation
Set the host ip in `HOST` and the host port in `PORT`.

### Launch
To launch the client simply use `make client`.

## Ressources
### Libraries
- P5: https://p5.readthedocs.io/en/latest/index.html
- socket: https://docs.python.org/fr/3/howto/sockets.html
- threading: https://docs.python.org/fr/3.8/library/threading.html 