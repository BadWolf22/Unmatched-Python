import random

class Character:
    def __init__(self, maxHealth = 0, moveDistance = 0, attackType = "", name = "", specialAbility = ""):
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.moveDistance = moveDistance
        self.attackType = attackType
        self.name = name
        self.specialAbility = specialAbility

    def loseHealth(self, damageTaken):
        self.health -= damageTaken
    def gainHealth(self, lifeGained):
        self.health += lifeGained

    def boostMovement(self, boostValue):
        self.moveDistance += boostValue