import random
from card import Deck

class AttackRange:
    melee = 0
    ranged = 1

class Character:
    def __init__(self, maxHealth = 0, moveDistance = 2, attackType = AttackRange.melee, name = "", specialAbility = ""):
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.moveDistance = moveDistance
        self.attackType = attackType
        self.name = name
        self.specialAbility = specialAbility
        self.deck = Deck()

    def loseHealth(self, damageTaken):
        self.health -= damageTaken
    def gainHealth(self, lifeGained):
        self.health += lifeGained

    def takeTurn(self):
        turns = 2
        while (turns > 0):
            # TODO: Options are movement (boostable), scheme, or attack (if player in range)
            # Actions may be cancelled before fully performed (before revealed)
            turns -= 1

    def boostMovement(self, boostValue):
        self.moveDistance += boostValue