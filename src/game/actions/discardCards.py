
from game.actions.iAction import IAction
from game.actions.moveCards import MoveCards


class DiscardCards(IAction):

    def __init__(self, player, indicies):
        self._hand = player.hand
        self._graveyard = player.graveyard
        self._indicies = indicies

    def execute(self):
        try:
            if self._hand.isEmpty():
                raise ValueError("hand is empty")

            text = ""
            self._indicies = sorted(self._indicies, reverse=True)

            for index in self._indicies:
                if index < 0 or index >= self._hand.numberOfCards:
                    raise IndexError("Error, index " + str(index) + " in hand does not exist")

                text +=             self._hand.getCard(index).cardName + ", "
                move = MoveCards(self._hand, [index], self._graveyard)
                move.execute()

            text = text.rstrip(", ")
            return text
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
