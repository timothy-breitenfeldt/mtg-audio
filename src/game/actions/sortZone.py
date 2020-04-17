
import random
import operator

from game.actions.iAction import IAction


class SortZone(IAction):

    def __init__(self, zone, properties):
        self._zone = zone
        self._properties = properties

    def execute(self):
        try:
            if self._properties == []:
                raise ValueError("Error, trying to sort " + self._zone.name + ", List of properties can not be empty")

            if self._zone.numberOfCards > 1:
                self._zone.cardContainer.sort(key=operator.attrgetter(*self._properties))
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
