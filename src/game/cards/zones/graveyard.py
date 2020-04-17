
from game.cards.zones.zone import Zone


class Graveyard(Zone):

    def __init__(self, graveyard=[]):
        super().__init__("Graveyard", graveyard)
