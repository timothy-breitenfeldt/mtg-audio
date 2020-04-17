
from game.actions.iAction import IAction


class SearchDatabase(IAction):

    def __init__(self, dbManager, searchParameters):
        self._dbManager = dbManager
        self._searchParameters = searchParameters

    def execute(self):
        try:
            if self._searchParameters == []:
                raise ValueError("Error, search parameters can not be empty")

            cards = []
            cardsStr = ""

            self._dbManager.connect()
            cards = self._dbManager.searchForCards(self._searchParameters)
            self._dbManager.close()

            if cards == []:
                raise LookupError("No results")

            for card in cards:
                cardsStr += card.__str__() + "\n\n"

            cardsStr = "Found " + str(len(cards)) + " results\n\n" + cardsStr
            cardsStr = cardsStr.rstrip(" \n\r")
            return cardsStr
        except Exception as e:
            raise e

    def undo(self):
        pass

    def redo(self):
        pass
