
from game.actions.iAction import IAction
from game.actions.tapCards import TapCards


class AttackWithCreatures(IAction):

    def __init__(self, player, indicies):
        self._creatures = player.creatures
        self._indicies = indicies

    def execute(self):
        try:
            if self._creatures.isEmpty():
                raise ValueError("creatures is empty")

            text = ""
            self._indicies = sorted(self._indicies, reverse=True)

            for index in self._indicies:
                if index < 0 or index >= self._creatures.numberOfCards:
                    raise IndexError("Error, index " + str(index) + " in creatures does not exist")

                text +=             self._creatures.getCard(index).cardName + ", "
                tap = TapCards(self._creatures, [index])
                tap.execute()

            text = text.rstrip(", ")
            return text
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
