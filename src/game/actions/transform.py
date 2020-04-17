
from game.actions.iAction import IAction 


class Transform(IAction):

    def __init__(self, zone, index):
        self._zone = zone
        self._index = index

    def execute(self):
        try:
            card = self._zone.getCard(self._index)

            if card.transformation is None:
                raise ValueError("Given card can not transform.")

            self._zone.flipCard(self._index)
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
