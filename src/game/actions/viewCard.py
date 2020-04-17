
from game.actions.iAction import IAction


class ViewCard(IAction):

    def __init__(self, zone, index):
        self._zone = zone
        self._index = index

    def execute(self):
        try:
            size = self._zone.numberOfCards

            if self._index < 0 or self._index >= size:
                raise IndexError(str(self._index) + " is not an index found in the zone " + self._zone.name)

            card = self._zone.getCard(self._index)
            return card.__str__()
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
