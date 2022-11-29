import random
import pygame
import pygame_gui
import json

# card dimensions
CARD_X = 160
CARD_Y = 220

class Deck:
    def __init__(self, size= 30):
        self.deckSize = size
        self.drawPile = list()
        self.discardPile = list()
        self.hand = list()
    def addCard(self, card):
        self.drawPile.append(card)
    def draw(self):
        # IMPORTANT
        # When drawing, physical cards should be added to either the "playerHand" or "enemyHand" widget.
        # Get the widget using https://pygame-menu.readthedocs.io/en/4.2.8/_source/create_menu.html?highlight=get%20widget#pygame_menu.menu.Menu.get_widget
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

    def assignDeck(jsonFile):

        newDeck = Deck(30)

        cardCount = 0
        cardIndex = 0
        while cardCount < newDeck.deckSize:
            newCard = Card.assignCard(jsonFile, cardIndex)

            copiesCount = 0
            while copiesCount < newCard.copies:
                newDeck.addCard(newCard)
                copiesCount += 1
                cardCount += 1
            
            cardIndex += 1

        print(len(newDeck.drawPile))
        return newDeck

            


    def getDeckImage(manager):
        
        # create card image dimensions and margins
        card_rect = pygame.Rect((0, 0), (CARD_X, CARD_Y))
        card_rect.bottomright = (-250, -150)

        # backside of card (Change later to put in character's cardback image)
        cardBack = pygame.image.load("characters/paganini.jpg").convert()

        # create the image ui object
        drawDeckImage = pygame_gui.elements.UIImage(relative_rect=card_rect,
                                                    image_surface=cardBack,
                                                    manager=manager,
                                                    anchors={'right': 'right',
                                                            'bottom': 'bottom'})
        return drawDeckImage

    def getDeckText(manager):

        # Create text
        #textColor = (255, 255, 255)
        #textFont = pygame.font.SysFont('Corbel',45, True)
        #text = textFont.render('Deck' , True , textColor)
        text_rect = pygame.Rect((0, 0), (200, 100))
        text_rect.bottomright = (-230, -220)

        drawDeckText = pygame_gui.elements.UILabel(relative_rect=text_rect,
                                                   text="Deck",  
                                                   manager=manager,
                                                   anchors={'right': 'right',
                                                            'bottom': 'bottom'})
        return drawDeckText

        

class Card:
    def __init__(self, name="", basicText="", immediateText="", duringText="", afterText="", value=0, pic="", boost=0, copies=0, type="", usableBy=""):
        self.name = name
        self.picture = pic
        self.boostValue = boost
        self.basicText = basicText
        self.immediateText = immediateText
        self.duringText = duringText
        self.afterText = afterText
        self.copies = copies
        self.value = value
        self.type = type
        self.usableBy = usableBy

    def assignCard(jsonFile, cardIndex):
        with open(jsonFile) as json_file:
            cardData = json.load(json_file)
        
        newCard = Card(
            name= cardData['cards'][cardIndex]['title'],
            copies= cardData['cards'][cardIndex]['quantity'],
            type= cardData['cards'][cardIndex]['type'],
            pic= cardData['cards'][cardIndex]['imageUrl'],
            boost= cardData['cards'][cardIndex]['boost'],
            basicText= cardData['cards'][cardIndex]['basicText'],
            immediateText= cardData['cards'][cardIndex]['immediateText'],
            duringText= cardData['cards'][cardIndex]['duringText'],
            afterText= cardData['cards'][cardIndex]['afterText'],
            value= cardData['cards'][cardIndex]['value'],
            usableBy= cardData['cards'][cardIndex]['characterName']
        )
        print(newCard.name)

        return newCard
