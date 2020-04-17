
from game.actions.iAction import IAction
from game.actions.moveCards import MoveCards


class MillCards(IAction):

    def __init__(self, player, numberOfCards):
        self._graveyard = player.graveyard
        self._library = player.library 
        self._numberOfCards = numberOfCards

    def execute(self):
        try:
            if self._numberOfCards > self._library.numberOfCards:
                raise ValueError("You don't have that many cards left in your library")

            text = ""

            for index in range(self._numberOfCards):
                text +=             self._library.getCard(1).cardName + ", "
                move = MoveCards(self._library, [1], self._graveyard)
                move.execute()

            text = text.rstrip(", ")
            return text
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
