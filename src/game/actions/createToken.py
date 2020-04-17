
from game.actions .iAction import IAction
from game.cards import Token
from game.cards.zones.creature import Creature
from game.cards.zones.land import Land
from game.cards.zones.other import Other


class CreateToken(IAction):

    def __init__(self, zone, cardName, type, text, power, toughness):
        self._zone = zone
        self._cardName = cardName
        self._type = type
        self._text = text
        self._power = power
        self._toughness = toughness

    def execute(self):
        try:
            if not isinstance(self._zone, Creature) and not isinstance(self._zone, Land) and not isinstance(self._zone, Other):
                raise TypeError("A token can only be created on the battlefield, in creature, land, or other  zones.")

            token = Token(self._cardName, self._type, self._text, self._power, self._toughness)
            self._zone.add(token)
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
