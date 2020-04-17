
from game.actions.iAction import IAction
from game.actions.moveCards import MoveCards


class PlayCardsInZone(IAction):

    def __init__(self, player, indicies, destinationZone):
        self._hand = player.hand
        self._indicies = indicies
        self._destinationZone = destinationZone

    def execute(self):
        try:
            text = "played "
            self._indicies = sorted(self._indicies, reverse=True)

            for index in self._indicies:
                if index < 0 or index >= self._hand.numberOfCards:
                    raise IndexError("Error, index " + str(index) + " in hand does not exist")

                text +=             self._hand.getCard(index).cardName + ", "
                move = MoveCards(self._hand, [index], self._destinationZone)
                move.execute()

            text = text.rstrip(", ")
            text += " in " + self._destinationZone.name
            return text
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
