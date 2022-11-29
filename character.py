import random
import json
from card import Deck

class AttackRange:
    isRanged = True



class Character:
    def __init__(self, maxHealth = 0, moveDistance = 2, attackType = AttackRange.isRanged, name = "", specialAbility = ""):
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.moveDistance = moveDistance
        self.attackType = attackType
        self.name = name
        self.specialAbility = specialAbility
        self.deck = Deck()
        self.hasScheme = False

    def loseHealth(self, damageTaken):
        self.health -= damageTaken
    def gainHealth(self, lifeGained):
        self.health += lifeGained

    def assignCharacter(jsonFile):
        with open(jsonFile) as json_file:
            characterData = json.load(json_file)

        newCharacter = Character(
            maxHealth= characterData['hero']['hp'],
            moveDistance= characterData['hero']['move'],
            attackType= characterData['hero']['isRanged'],
            name= characterData['hero']['name'],
            specialAbility= characterData['hero']['specialAbility']
        )
        print(newCharacter.name)
        print(newCharacter.health)
        print(newCharacter.moveDistance)
        print(newCharacter.attackType)
        print(newCharacter.specialAbility)

        return newCharacter



    #Taking turns
    def takeTurn(self):
        turns = 2
        while (turns > 0):
            # TODO: Options are movement (boostable), scheme, or attack (if player in range)
            # Actions may be cancelled before fully performed (before revealed)
            

            turns -= 1

    def boostMovement(self, boostValue):
        self.moveDistance += boostValue