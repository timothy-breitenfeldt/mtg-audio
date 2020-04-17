
from game.actions.iAction import IAction
from game.actions.moveCards import MoveCards


class DrawCards(IAction):

    def __init__(self, player, numberOfCards):
        self._hand = player.hand
        self._library = player.library 
        self._numberOfCards = numberOfCards

    def execute(self):
        try:
            if self._numberOfCards > self._library.numberOfCards:
                raise ValueError("You don't have that many cards left in your library")

            text = ""

            for counter in range(self._numberOfCards):
                text +=             self._library.getCard(0).cardName + ", "
                move = MoveCards(self._library, [0], self._hand)
                move.execute()

            text = text.rstrip(", ")
            return text
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
