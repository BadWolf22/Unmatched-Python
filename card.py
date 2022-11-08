import random

class CardType:
    defense = 0
    attack = 1
    versatile = 2
    special = 3

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