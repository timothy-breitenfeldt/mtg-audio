
from game.actions.iAction import IAction


class TapZone(IAction):

    def __init__(self, zone):
        self._zone = zone

    def execute(self):
        try:
            for index in range(self._zone.numberOfCards):
                card = self._zone.getCard(index)
                card.tapped = "tapped"
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
