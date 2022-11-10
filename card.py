import random
import pygame

# activate the pygame library 
pygame.init()

# card dimensions
CARD_X = 411
CARD_Y = 561

class CardType:
    defense = 0
    attack = 1
    versatile = 2
    special = 3
    scheme = 4

class Deck:
    def __init__(self):
        self.drawPile = list()
        self.discardPile = list()
        self.hand = list()
    def addCard(self, card):
        self.drawPile.append(card)
    def draw(self):
        if len(self.drawPile == 0):
            return -1
        chosen = random.choice(self.drawPile)
        self.drawPile.remove(chosen)
        self.hand.append(chosen)
        return chosen
    def discard(self, card=None):
        if not card:
            if len(self.hand) == 0:
                return -1
            card = random.choice(self.hand)
        self.hand.remove(card)
        self.discardPile.append(card)
    def play(self, card):
        # Here be play steps
        self.discard(card)

    def displayDeck():
        # create the display surface object
        # of specific dimension..e(X, Y).
        scrn = pygame.display.set_mode((CARD_X, CARD_Y))

        # set the pygame window name
        pygame.display.set_caption('image')
        
        # change later so displays the character's cardback
        imp = pygame.image.load("characters\paganini.jpg").convert()
        
        # Using blit to copy content from one surface to other
        scrn.blit(imp, (500, 500))
        
        # paint screen one time
        pygame.display.flip()
        status = True
        while (status):
        
            # iterate over the list of Event objects
            # that was returned by pygame.event.get() method.
            for i in pygame.event.get():
        
                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if i.type == pygame.QUIT:
                    status = False
        

class Card:
    def __init__(self, name="", desc="", value=0, pic="", boost=0, copies=0, type=CardType.versatile, boostable=False):
        self.name = name
        self.picture = pic
        self.boostValue = boost
        self.description = desc
        self.copies = copies
        self.value = value
        self.type = type
        self.boostable = boostable