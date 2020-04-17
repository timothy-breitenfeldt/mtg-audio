
from game.cards.zones.zone import Zone 
from game.cards.card import Card


class Other(Zone):

    def __init__(self, otherSpells=[]):
        super().__init__("Other Spells", otherSpells)

    # Override
    def add(self, card, index=-1):
        if card == None:
            raise ValueError("Error, invalid value for card")
        if index < -1 or index > self._numberOfCards:
            raise IndexError("Error trying to add card by index to " + self.name + ", index " + str(index) + " is out of bounds")
        if not isinstance(card, Card):
            raise TypeError("Error, given object must be of type Card")

        self.cardContainer.insert(index, card)
        self.numberOfCards += 1
        return card