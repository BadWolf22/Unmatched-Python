import card
import character
import simple
import pygame
import random

# actions
move = False
playScheme = False
attack = False

# players
player1 = simple.players["player"]
player2 = simple.players["player"]

def startGame():

    print("Game Started")
    # each player draws 7 cards
    count = 0
    while count < 7:
        player1.deck.draw()
        player2.deck.draw()
        count += 1


    # while win conditions == false:

    # player 1 goes first
    playTurn(player1)

    # player 2 goes second
    playTurn(player2)


def playTurn(player):
    
    # create menu with choices of what to do on turn


    while True:

        if move == True:
            move=False
            # do move action
            moveAction(player)
            return
     
        if playScheme == True:
            playScheme=False
            # play scheme card
            playSchemeAction(player)
            return

        if attack == True:
            attack=False
            # play attack card
            attackAction(player)
            return


def moveAction(player):
    maxDistance = player.moveDistance

    # code for choosing how many spaces to move


    # draw a card
    player.deck.draw()

    return

def playSchemeAction(player):
    return

def attackAction(player):
    return
    