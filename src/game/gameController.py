
from game.player import Player
from game.databaseManager import DatabaseManager
from game.actions.iAction import IAction
from game.actions import *


class GameController:

    def __init__(self):
        # eventually read UserSettings table in database for username, to pass to player.
        self._player = Player()
        self._dbManager = DatabaseManager()
        self._actionStack = []

    @property
    def player(self):
        return self._player 

    def undo(self, index):
        self._actionStack[index].undo()

    def redo(self, index):
        self._actionStack[index].redo()

    def push(self, action):
        if not isinstance(action, IAction):
            raise TypeError("Given object " + action + " must be of type IAction.")

        if len(self._actionStack) == 25:
            self._actionStack.pop(0)
            
        self._actionStack.append(action)

    def loadDeck(self, filename):
        try:
            action = LoadDeck(self._dbManager, self._player, filename)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def viewBattlefield(self):
        try:
            action = ViewBattlefield(self._player)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def viewBattlefieldWithInfo(self):
        try:
            action = ViewBattlefieldWithInfo(self._player)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def viewCard(self, zone, index):
        try:
            action = ViewCard(zone, index)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def viewCardNames(self, zone):
        try:
            action = ViewCardNames(self._player, zone)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def viewCardsAndInfo(self, zone):
        try:
            action = ViewCardsAndInfo(self._player, zone)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def moveCards(self, sourceZone, indicies, destinationZone):
        try:
            action = MoveCards(sourceZone, indicies, destinationZone)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def moveZone(self, sourceZone, destinationZone):
        try:
            action = MoveZone(sourceZone, destinationZone)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def tapCards(self, zone, indicies):
        try:
            action = TapCards(zone, indicies)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def tapZone(self, zone):
        try:
            action = TapZone(zone)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def tapBattlefield(self):
        try:
            action = TapBattlefield(self._player)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def untapCards(self, zone, indicies):
        try:
            action = UntapCards(zone, indicies)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def untapZone(self, zone):
        try:
            action = UntapZone(zone)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def untapBattlefield(self):
        try:
            action = UntapBattlefield(self._player)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def shuffleZone(self, zone):
        try:
            action = ShuffleZone(zone)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def sortZone(self, zone, properties):
        try:
            action = SortZone(zone, properties)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def cleanup(self):
        try:
            action = Cleanup(self._player)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def searchDatabase(self, searchParameters):
        try:
            action = SearchDatabase(self._dbManager, searchParameters)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def playCardsInZone(self, indicies, destinationZone):
        try:
            action = PlayCardsInZone(self._player, indicies, destinationZone)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def playCardsAutoPlacement(self, sourceZone, indicies):
        try:
            action = PlayCardsAutoPlacement(sourceZone, self._player, indicies)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def drawCards(self, numberOfCards):
        try:
            action = DrawCards(self._player, numberOfCards)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def discardCards(self, indicies):
        try:
            action = DiscardCards(self._player, indicies)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def millCards(self, numberOfCards):
        try:
            action = MillCards(self._player, numberOfCards)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def attackWithCreatures(self, indicies):
        try:
            action = AttackWithCreatures(self._player, indicies)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def attackWithAllCreatures(self):
        try:
            action = AttackWithAllCreatures(self._player)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def swapCards(self, zone, index1, index2):
        try:
            action = SwapCards(zone, index1, index2)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def swapZones(self, zone1, zone2):
        try:
            action = SwapZones(zone1, zone2)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def transform(self, zone, index):
        try:
            action = Transform(zone, index)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def createToken(self, zone, cardName, type="", power="", toughness="", text=""):
        try:
            action = CreateToken(zone, cardName, type, text, power, toughness)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def addCounters(self, zone, index, counters):
        try:
            action = AddCounters(zone, index, counters)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def subtractCounters(self, zone, index, counters):
        try:
            action = SubtractCounters(zone, index, counters)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def addPlus1Counters(self, zone, index, plus1Counters):
        try:
            action = AddPlus1Counters(zone, index, plus1Counters)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def subtractPlus1Counters(self, zone, index, plus1Counters):
        try:
            action = SubtractPlus1Counters(zone, index, plus1Counters)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def addMinus1Counters(self, zone, index, minus1Counters):
        try:
            action = AddMinus1Counters(zone, index, minus1Counters)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e

    def subtractMinus1Counters(self, zone, index, minus1Counters):
        try:
            action = SubtractMinus1Counters(zone, index, minus1Counters)
            self.push(action)
            return action.execute()
        except Exception as e:
            raise e
