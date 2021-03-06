
from game.actions.iAction import IAction  


class SubtractPlus1Counters(IAction):

    def __init__(self, zone, index, plus1Counters):
        self._zone = zone
        self._index = index
        self._plus1Counters = plus1Counters

    def execute(self):
        try:
            card = self._zone.getCard(self._index)

            if self._plus1Counters <= 0:
                raise ValueError("Please provide a positive non-zero number to subtract plus 1 counters.")

            if card.plus1Counters - self._plus1Counters < 0:
                raise ValueError("Plus 1 counters can not be negative.")
            else:
                card.plus1Counters -= self._plus1Counters

                if card.transformation is not None and card.transformation != "":
                    card.transformation.plus1Counters -= self._plus1Counters

        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
