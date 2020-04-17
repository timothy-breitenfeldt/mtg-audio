
from game.actions.iAction import IAction  


class AddMinus1Counters(IAction):

    def __init__(self, zone, index, minus1Counters):
        self._zone = zone
        self._index = index
        self._minus1Counters = minus1Counters

    def execute(self):
        try:
            card = self._zone.getCard(self._index)

            if self._minus1Counters <= 0:
                raise ValueError("Please provide a positive non-zero number to add minus 1 counters.")

            card.minus1Counters += self._minus1Counters

            if card.transformation is not None and card.transformation != "":
                card.transformation.minus1Counters += self._minus1Counters

        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
