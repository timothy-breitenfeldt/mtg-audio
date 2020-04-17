
from game.actions.iAction import IAction


class ViewCardNames(IAction):

    def __init__(self, player, zone):
        self._player = player
        self._zone = zone

    def execute(self):
        try:
            return self._zone.getCardNames()
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
