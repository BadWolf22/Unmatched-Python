import random

import pygame
from pygame.locals import *

from card import Deck

# import json

WIDTH = 1920
HEIGHT = 1080
MARGIN = 800
PADDING = 25
COL_PART = 10
ROW_PART = 5

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((51, 51, 51))

    map = Map()
    Deck.displayDeck()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_SPACE: map = Map()
                if event.key == K_ESCAPE: return
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
                if random.random() < 0.3: self.randomNode(r, c)
        self.autoConnect()
    def randomNode(self, r, c):
        x = random.randint(int((WIDTH-MARGIN)/COL_PART*c)+PADDING, int((WIDTH-MARGIN)/COL_PART*(c+1))-PADDING) + MARGIN/2
        y = random.randint(int((HEIGHT-MARGIN)/ROW_PART*r)+PADDING, int((HEIGHT-MARGIN)/ROW_PART*(r+1))-PADDING) + MARGIN/2
        self.nodes.append(Node((x,y)))
    def display(self, screen):
        for node in self.nodes:
            # here we will draw all of the paths first
            for neighbor in node.neighbors:
                pygame.draw.line(screen, 0, node.pos, neighbor.pos)
        for node in self.nodes:
            pygame.draw.circle(screen, 255, (node.pos[0],node.pos[1]), 15)
    def isConnected(self):
        visited = set()
        stack = set()
        stack.add(random.choice(self.nodes))
        while (len(stack) > 0):
            curr = stack.pop()
            visited.add(curr)
            for neighbor in curr.neighbors:
                if neighbor not in visited: stack.add(neighbor)
        return len(visited) == len(self.nodes)
    def autoConnect(self):
        # My initial strategy is to connect the two closest nodes until there is only one part in the graph.
        # TODO: Improve (or implement a hardcoded map)
        while (not self.isConnected()):
            closestDist = float("inf")
            for first in self.nodes:
                for second in self.nodes:
                    if first == second: continue # same node
                    if len(first.neighbors.intersection(set([second]))) != 0: continue # already neighbors
                    dX = second.pos[0] - first.pos[0]
                    dY = second.pos[1] - first.pos[1]
                    sqDist = dX**2 + dY**2
                    if (sqDist < closestDist): 
                        closestDist = sqDist
                        closest = (first, second)
            closest[0].addNeighbor(closest[1])


class Node:
    def __init__(self, pos):
        self.neighbors = set()
        self.pos = pos
        self.sections = list()
    def addNeighbor(self, neighbor):
        self.neighbors.add(neighbor)
        neighbor.neighbors.add(self)

if __name__ == "__main__":
    main()