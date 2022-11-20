import random
import pygame
import pygame_gui



class startTurn:

    actions = list('move', 'attack', 'play scheme')

    def takeAction():

        # rectangle for selection list
        rectangle = pygame.Rect((600, ))
        actionSelectionList = pygame_gui.elements.UISelectionList()