import random
import pygame

# card dimensions
CARD_X = 411
CARD_Y = 561

class CardType:
    defense = 0
    attack = 1
    versatile = 2
    special = 3
    scheme = 4
class Usabilities:
    any = 0
    main = 1
    sidekick = 2

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

    def getDeckImage():
        
        # Create text
        textColor = (255, 255, 255)
        textFont = pygame.font.SysFont('Corbel',45, True)
        text = textFont.render('Deck' , True , textColor)

        # change later so displays the character's cardback
        deckImage = pygame.image.load("characters\paganini.jpg").convert()

        #Decrease size of image
        deckImage = pygame.transform.scale(deckImage, (411/2.5, 561/2.5))


        
        return [deckImage, text]
        

class Card:
    def __init__(self, name="", desc="", value=0, pic="", boost=0, copies=0, type=CardType.versatile, boostable=False, usableBy=Usabilities.any):
        self.name = name
        self.picture = pic
        self.boostValue = boost
        self.description = desc
        self.copies = copies
        self.value = value
        self.type = type
        self.boostable = boostable
        self.usableBy = usableBy