
import random
import operator

from game.cards import Card


class Zone(object):

    def __init__(self, name, cards):
        self._name = name
        self._cardContainer = cards
        self._numberOfCards = 0
        self._position = 0

    @property
    def name(self):
        return self._name

    @property
    def cardContainer(self):
        return self._cardContainer

    @property
    def numberOfCards(self):
        return self._numberOfCards

    @property
    def position(self):
        return self._position

    @property
    def currentCard(self):
        if self._numberOfCards == 0:
            return None

        return self._cardContainer[self._position]

    @numberOfCards.setter
    def numberOfCards(self, num):
        if num < 0:
            raise ValueError("Error trying to set numberOfCards, this variable can not be less than 0")

        self._numberOfCards = num

    @position.setter
    def position(self, position):
        self._position = position

    @cardContainer.setter
    def cardContainer(self, cards):
        if cards is None:
            raise ValueError("Error trying to set cardContainer in " + self.name + ", it can not be None")

        self._cardContainer = cards

    def resetPosition(self):
        self._position = 0

    def next(self):
        if self._position ==0 and self._numberOfCards == 1:
            return self.currentCard
        if (self._position + 1) >= self._numberOfCards:
            return None

        self._position += 1
        return self.currentCard

    def previous(self):
        if self._position == 0 and self._numberOfCards == 1:
            return self.currentCard
        if (self._position - 1) < 0:
            return None

        self._position -= 1
        return self.currentCard

    def add(self, card, index=-1):
        if card == None:
            raise ValueError("Error, invalid value for card")
        if index < -1 or index > self._numberOfCards:
            raise IndexError("Error trying to add card by index to " + self.name + ", index " + str(index) + " is out of bounds")
        if not isinstance(card, Card):
            raise TypeError("Error, given object must be of type Card")

        if not card.frontFacing:
            card = card.transformation

        card.tapped = ""
        card.counters = 0
        card.plus1Counters = 0
        card.minus1Counters = 0
        self.cardContainer.insert(index, card)
        self.numberOfCards += 1
        return card

    def remove(self, index=0):
        if index < 0 or index >= self._numberOfCards:
            raise IndexError("Error trying to remove card by index from " + self.name + ", index is out of bounds")

        self._numberOfCards -= 1

        if self._position == self._numberOfCards and self._position != 0:
            self._position -= 1

        return self._cardContainer.pop(index)

    def getCard(self, index):
        if index < 0 or index >= self._numberOfCards:
            raise IndexError("Error trying to get card from " + self.name + ", index " + str(index) + " is out of bounds")

        return self.cardContainer[index]

    def setCard(self, index, card):
        if index < 0 or index >= self._numberOfCards:
            raise IndexError("Error trying to get card from " + self.name + ", index " + str(index) + " is out of bounds")

        self.cardContainer[index] = card

    def flipCard(self, index):
        self._cardContainer[index] = self._cardContainer[index].transformation

    def search(self, searchName):
        v = searchName.strip(" \t\n\r").lower()

        for index in range(self.numberOfCards):
            card = self.getCard(index)
            name = card.cardName.lower()

            if name == v:
                return index

        return -1

    def isEmpty(self):
        return (self._numberOfCards == 0)

    def clearZone(self):
        self._cardContainer = []
        self._numberOfCards = 0

    def getCardNames(self):
        text = ""

        for index in range(self.numberOfCards):
            text += str(index + 1) + " " + self.getCardName(index) + ",\n"

        if text == "":
            text += "empty"

        return self.name + "\n" + text.rstrip("\n")

    def getCardNamesAndInfo(self):
        text = ""

        for index in range(self.numberOfCards):
            card = self.getCard(index)
            text += str(index + 1) + " " + self.getCardName() + ", " + card.manaCost + " " + card.powerAndToughness + ",\n"

        if text == "":
            text += "empty"

        return self.name + "\n" + text.rstrip("\n")

    def getCardName(self, index=-1):
        card = None
        text = ""

        if index == -1:
            card = self.currentCard
        else:
            card = self.getCard(index)

        text = card.cardName

        if card.tapped != "":
            text += ", " + card.tapped
        if card.counters > 0:
            text += ", " + str(card.counters) + " counters"
        if card.plus1Counters > 0:
            text += ", " + str(card.plus1Counters) + " plus 1 counters"
        if card.minus1Counters > 0:
            text += ", " + str(card.minus1Counters) + " minus 1 counters"

        return text


