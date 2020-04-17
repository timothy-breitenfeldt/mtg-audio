
from game.actions.iAction import IAction


class UntapCards(IAction):

    def __init__(self, zone, indicies):
        self._zone = zone
        self._indicies = indicies

    def execute(self):
        try:
            for index in self._indicies:
                if index < 0 or index >=self._zone.numberOfCards:
                    raise IndexError("Error, index " + str(self._index) + " in " + self._zone + " does not exist")

                card = self._zone.getCard(index)
                card.tapped = ""
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
