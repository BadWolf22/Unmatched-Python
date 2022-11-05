import pygame
from pygame.locals import *
import random
import json

WIDTH = 800
HEIGHT = 600
COL_PART = 8
ROW_PART = 6

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((51, 51, 51))

    map = Map()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.blit(background, (0, 0))
        # pygame.draw.line(screen,(255,255,255),(0, 0),pygame.mouse.get_pos())
        map.display(screen)
        # pygame.draw.circle(screen,255,(random.randint(0,800),random.randint(0,600)),random.randint(5,15))
        pygame.display.flip()

class Map:
    def __init__(self):
        self.nodes = list()
        for r in range(ROW_PART):
            for c in range(COL_PART):
                if random.random() < 0.4: self.randomNode(r, c)
    def randomNode(self, r, c):
        x = random.randint(int(WIDTH/COL_PART*c), int(WIDTH/COL_PART*(c+1)))
        y = random.randint(int(HEIGHT/ROW_PART*r), int(HEIGHT/ROW_PART*(r+1)))
        self.nodes.append(Node((x,y)))
    def display(self, screen):
        for node in self.nodes:
            pygame.draw.circle(screen, 255, (node.pos[0],node.pos[1]), 15)

class Node:
    def __init__(self, pos):
        self.neighbors = set()
        self.pos = pos
    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)
        neighbor.neighbors.append(self)

if __name__ == "__main__":
    main()