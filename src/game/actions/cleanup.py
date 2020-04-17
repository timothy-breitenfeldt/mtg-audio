
from game.actions.iAction import IAction
from game.actions.moveZone import MoveZone


class Cleanup(IAction):

    def __init__(self, player):
        self._player = player

    def execute(self):
        try:
            cleanupHandAction = MoveZone(self._player.hand, self._player.library)
            cleanupCreaturesAction = MoveZone(self._player.creatures, self._player.library)
            cleanupOtherSpellsAction = MoveZone(self._player.otherSpells, self._player.library)
            cleanupLandsAction = MoveZone(self._player.lands, self._player.library)
            cleanupExileAction = MoveZone(self._player.exile, self._player.library)
            cleanupGraveyardAction = MoveZone(self._player.graveyard, self._player.library)
            zones = (self._player.hand, self._player.graveyard, self._player.exile,
                    self._player.creatures, self._player.lands, self._player.otherSpells)

            cleanupHandAction.execute()
            cleanupCreaturesAction.execute()
            cleanupOtherSpellsAction.execute()
            cleanupLandsAction.execute()
            cleanupExileAction.execute()
            cleanupGraveyardAction.execute()

            for zone in zones:
                zone.clearZone()
                zone.resetPosition()

            self._player.life = 20
            self._player.energy = 0
            self._player.library.numberOfCards = len(self._player.library.cardContainer)
            self._player.library.resetPosition()
        except Exception as e:
            raise e    

    def undo(self):
        pass

    def redo(self):
        pass
