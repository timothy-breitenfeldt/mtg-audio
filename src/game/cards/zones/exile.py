
from game.cards.zones.zone import Zone 


class Exile(Zone):

    def __init__(self, exile=[]):
        super().__init__("Exile", exile)    

