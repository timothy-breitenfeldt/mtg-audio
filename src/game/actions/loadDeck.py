
from sqlite3 import OperationalError
import re

from game.actions.iAction import IAction
from game.actions.cleanup import Cleanup

class LoadDeck(IAction):

    def __init__(self, dbManager, player, filename):
        self._dbManager = dbManager
        self._player = player
        self._filename = filename 

    def execute(self):
        try:
            if self._filename == "" or self._filename is None:
                raise ValueError("Error, filename in loadDeck must be a valid string")

            nameDictionary = {}
            card = None

            self._player.clearAllZones()
            self._dbManager.connect()

            with open("decks/" + self._filename, "r") as deck:
                deckString = deck.read()
                deckString = deckString.replace("'", "\\'")
                deckString = deckString.replace("\"", "\\\"")
                deckString = self._commentRemover(deckString)
                deckString = deckString.replace("\\", "")
                deckList = iter(deckString.split("\n"))

                for cardName in deckList:
                    cardName = cardName.strip(" \n\t\r").lower()

                    if cardName == "":
                        continue

                    # Check if the card has been cashed already 
                    if cardName in nameDictionary:
                        card = nameDictionary[cardName]
                        clonedCard = card.clone()
                        self._player.library.add(clonedCard, self._player.library.numberOfCards)
                        continue

                    card = self._dbManager.searchByCardName(cardName)

                    if card == None:
                        self._dbManager.close()
                        raise LookupError("unable to find the card " + cardName)

                    self._player.library.add(card, self._player.library.numberOfCards)
                    nameDictionary[cardName] = card

            self._player.library.deckName = self._filename
            self._dbManager.close()
        except IOError as ioe:
            raise IOError("Error, unable to find the deck " + self._filename + ", make sure it is in the decks folder")
        except Exception as e:
            raise e

    def _commentRemover(self, text):
        """source: https://gist.github.com/ChunMinChang/88bfa5842396c1fbbc5b"""
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " " # note: a space and not an empty string
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        return re.sub(pattern, replacer, text)

    def undo(self):
        pass

    def redo(self):
        pass
