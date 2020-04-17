
from game.actions.iAction import IAction


class ViewBattlefield(IAction):

    def __init__(self, player):
        self._player = player

    def execute(self):
        try:
            creatures = self._player.creatures
            lands = self._player.lands
            otherSpells = self._player.otherSpells

            if creatures.isEmpty() and lands.isEmpty() and otherSpells.isEmpty():
                return "Battlefield is empty"

            text = ""

            text += creatures.getCardNames() + "\n"
            text += lands.getCardNames() + "\n"
            text += otherSpells.getCardNames()
            return text
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
