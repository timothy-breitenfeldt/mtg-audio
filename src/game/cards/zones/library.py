
from collections import deque
import random

from game.cards.zones.zone import Zone


class Library(Zone):

    def __init__(self, library=[]):
        super().__init__("Library", library)

        self._deckName = ""

    @property
    def deckName(self):
        return self._deckName

    @deckName.setter
    def deckName(self, deckName):
        if deckName == None:
            raise ValueError("Error, deckName can not be None")

        self._deckName = deckName