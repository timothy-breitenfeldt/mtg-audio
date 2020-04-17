
from game.actions.iAction import IAction
from game.cards.token import Token  


class MoveZone(IAction):

    def __init__(self, sourceZone, destinationZone):
        self._sourceZone = sourceZone
        self._destinationZone = destinationZone

    def execute(self):
        try:
            while self._sourceZone.numberOfCards > 0:
                card = self._sourceZone.remove()

                if not isinstance(card, Token):
                    self._destinationZone.add(card)

        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
