
from game.actions.iAction import IAction


class SwapCards(IAction):

    def __init__(self, zone, index1, index2):
        self._zone = zone
        self._index1 = index1
        self._index2 = index2

    def execute(self):
        try:
            if self._index1 < 0 or self._index1 >= self._zone.numberOfCards:
                raise IndexError("index1 is not found in this zone")
            if self._index2 < 0 or self._index2 >= self._zone.numberOfCards:
                raise IndexError("index2 is not found in this zone")

            card1 = self._zone.getCard(self._index1)
            card2 = self._zone.getCard(self._index2)
            self._zone.setCard(self._index2, card1)
            self._zone.setCard(self._index1, card2)
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
