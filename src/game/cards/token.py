
from game.cards.card import Card


class Token(Card):

    def __init__(self, cardName, type, text, power, toughness):
        super().__init__(cardName, "", "", type, "", "", "", text, "", power, toughness, "", "", "", "", None, True)
