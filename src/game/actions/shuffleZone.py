
import random

from game.actions.iAction import IAction


class ShuffleZone(IAction):

    def __init__(self, zone):
        self._zone = zone

    def execute(self):
        try:
            if self._zone.numberOfCards > 1:
                random.shuffle(self._zone.cardContainer)
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
