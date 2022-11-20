from map import Map
from globals import *

import pygame
from pygame.locals import *

from card import Deck

######################################
# Socket setup
import socketio
sio = socketio.Client()

@sio.event
def connect():
    print('connection established', f"sid=`{sio.get_sid()}`")

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on("message")
def my_message(sid, data):
    print(sid, "says:", data)
######################################

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(sio.get_sid())
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((51, 51, 51))

    map = Map()
    drawDeck = Deck.getDeckImage()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_SPACE: map = Map()
                if event.key == K_ESCAPE: return
                if event.key == K_m: sio.emit("message", "hiii")
        screen.blit(background, (0, 0))
        screen.blit(drawDeck[0], (1550, 730))
        screen.blit(drawDeck[1], (1590, 820))

        # pygame.draw.line(screen,(255,255,255),(0, 0),pygame.mouse.get_pos())
        map.display(screen, pygame)
        # pygame.draw.circle(screen,255,(random.randint(0,800),random.randint(0,600)),random.randint(5,15))
        pygame.display.flip()

# First connect to the server, begin the game client, then disconnect when the client is stopped
if __name__ == "__main__":
    sio.connect('http://localhost:5000')
    main()
    sio.disconnect()