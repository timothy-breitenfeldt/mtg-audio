
from game.actions.tapZone import TapZone
from game.actions.iAction import IAction


class AttackWithAllCreatures(IAction):

    def __init__(self, player):
        self._creatures = player.creatures

    def execute(self):
        try:
                tap = TapZone(self._creatures)
                tap.execute()
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
