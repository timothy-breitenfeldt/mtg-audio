
from game.actions.iAction import IAction 


class UntapBattlefield(IAction):

    def __init__(self, player):
        self._player = player

    def execute(self):
        try:
            creatures = self._player.creatures
            lands = self._player.lands
            otherSpells = self._player.otherSpells

            for index in range(creatures.numberOfCards):
                card = creatures.getCard(index)
                card.tapped = ""

            for index in range(lands.numberOfCards):
                card = lands.getCard(index)
                card.tapped = ""

            for index in range(otherSpells.numberOfCards):
                card = otherSpells.getCard(index)
                card.tapped = ""
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
