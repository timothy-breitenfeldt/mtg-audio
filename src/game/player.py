from game.cards.zones import Library
from game.cards.zones import Hand
from game.cards.zones import Graveyard
from game.cards.zones import Exile
from game.cards.zones import Creature
from game.cards.zones import Land
from game.cards.zones import Other


class Player:

    def __init__(self, username="", library=[], hand=[], graveyard=[], exile=[], lands=[], creatures=[], otherSpells=[]):
        self._username = username
        self._life = 20
        self._energy = 0
        self._library = Library(library)
        self._hand = Hand(hand)
        self._graveyard = Graveyard(graveyard)
        self._exile = Exile(exile)
        self._lands = Land(lands)
        self._creatures = Creature(creatures)
        self._otherSpells = Other(otherSpells)

    def clearAllZones(self):
        self._hand.clearZone()
        self._library.clearZone()
        self.graveyard.clearZone()
        self._exile.clearZone()
        self._creatures.clearZone()
        self._lands.clearZone()
        self._otherSpells.clearZone()

    @property
    def username(self):
        return self._username

    @property
    def life(self):
        return self._life

    @property
    def energy(self):
        return self._energy

    @property
    def library(self):
        return self._library

    @property
    def hand(self):
        return self._hand

    @property
    def graveyard(self):
        return self._graveyard

    @property
    def exile(self):
        return self._exile
    @property
    def lands(self):
        return self._lands

    @property
    def creatures(self):
        return self._creatures

    @property
    def otherSpells(self):
        return self._otherSpells

    @life.setter
    def life(self, life):
        self._life = life

    @energy.setter
    def energy(self, energy):
        self._energy = energy

