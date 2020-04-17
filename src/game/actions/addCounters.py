
from game.actions.iAction import IAction  


class AddCounters(IAction):

    def __init__(self, zone, index, counters):
        self._zone = zone
        self._index = index
        self._counters = counters

    def execute(self):
        try:
            card = self._zone.getCard(self._index)

            if self._counters <= 0:
                raise ValueError("Please provide a positive non-zero number to add counters.")

            card.counters += self._counters

            if card.transformation is not None and card.transformation != "":
                card.transformation.counters += self._counters

        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
