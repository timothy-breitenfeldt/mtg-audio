
from game.actions.iAction import IAction


class SwapZones(IAction):

    def __init__(self, zone1, zone2):
        self._zone1 = zone1
        self._zone2 = zone2

    def execute(self):
        print("zone1: " + self._zone1.name + "\nzone2: " + self._zone2.name)

        try:
            temp = self._zone1.cardContainer
            self._zone1.cardContainer = self._zone2.cardContainer
            self._zone2.cardContainer = temp

            temp = self._zone1.numberOfCards
            self._zone1.numberOfCards = self._zone2.numberOfCards
            self._zone2.numberOfCards = temp
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
