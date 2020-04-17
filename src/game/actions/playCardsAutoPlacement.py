
from game.actions.iAction import IAction


class PlayCardsAutoPlacement(IAction):

    def __init__(self, sourceZone, player, indicies):
        self._sourceZone = sourceZone
        self._indicies = indicies
        self._player = player

    def execute(self):
        try:
            # sort and reverse the list of indicies so that you don't violate the accuracy of the indicies.
            self._indicies = sorted(self._indicies, reverse=True)
            text = "played "

            for index in self._indicies:
                if index < 0 or index >= self._sourceZone.numberOfCards:
                    raise IndexError("Error, index " + str(index) + " in hand does not exist")

                card = self._sourceZone.remove(index)
                text +=             card.cardName + ", in "
                destinationZone = None
                cardType = card.type.lower()

                if "creature" in cardType:
                    destinationZone = self._player.creatures
                elif "land" in cardType:
                    destinationZone = self._player.lands
                elif "instant" in cardType or "sorcery" in cardType:
                    destinationZone = self._player.graveyard
                else:
                    destinationZone = self._player.otherSpells

                destinationZone.add(card)
                text += destinationZone.name + ", "

            text = text.rstrip(", ")
            return text
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
