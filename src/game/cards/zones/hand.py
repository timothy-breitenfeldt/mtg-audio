import operator

from game.cards.zones.zone import Zone
from game.actions import SortZone


class Hand(Zone):
    
    def __init__(self, hand=[]):
        super().__init__("Hand", hand)

    def add(self, card, index=-1):
        card = super().add(card, index)
        sortAction = SortZone(self, ["cmc", "type", "manaCost"])
        sortAction.execute()
        return card



