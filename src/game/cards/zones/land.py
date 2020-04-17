
import operator

from game.cards.zones.zone import Zone 
from game.actions.sortZone import SortZone
from game.cards.card import Card


class Land(Zone):

    def __init__(self, lands=[]):
        super().__init__("Lands", lands)    

    # Override zone method to build in an auto sort
    def add(self, card, index=-1):
        if card == None:
            raise ValueError("Error, invalid value for card")
        if index < -1 or index > self._numberOfCards:
            raise IndexError("Error trying to add card by index to " + self.name + ", index " + str(index) + " is out of bounds")
        if not isinstance(card, Card):
            raise TypeError("Error, given object must be of type Card")

        self.cardContainer.insert(index, card)
        self.numberOfCards += 1

        sortAction = SortZone(self, ["tapped", "type", "cardName"])
        sortAction.execute()
        return card
