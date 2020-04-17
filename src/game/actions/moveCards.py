
from game.actions.iAction import IAction
from game.cards.token import Token 


class MoveCards(IAction):

    def __init__(self, sourceZone, indicies, destinationZone):
        self._sourceZone = sourceZone
        self._indicies = indicies
        self._destinationZone = destinationZone

    def execute(self):
        try:
            killedToken = False
            cards = []

            # sort and reverse the list of indicies so that you don't violate the accuracy of the indicies.
            self._indicies = sorted(self._indicies, reverse=True)

            for index in self._indicies:
                if index < 0 or index >=self._sourceZone.numberOfCards:
                    raise IndexError("Error, index " + str(index) + " in hand does not exist")

                card = self._sourceZone.remove(index)
                cards.append(card)

                if not isinstance(card, Token):
                    self._destinationZone.add(card)

            return cards
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
