import os

import wx

from windows import ListBoxDialog
from windows import CreateTokenDialog
from windows import TextWindow


class GameManager:

    def __init__(self, gamePanel, controller, zoneTree, screenreader):
        self._screenreader = screenreader
        self._controller = controller
        self._zoneTree = zoneTree
        self._gamePanel = gamePanel
        self._libraryMoveMenu = self.createLibraryMoveMenu()

    def createLibraryMoveMenu(self):
        libraryMoveMenu = wx.Menu()
        moveToTopId = wx.NewId()
        moveToBottomId = wx.NewId()
        moveToOtherId = wx.NewId()

        libraryMoveMenu.Append(moveToTopId , "Top")
        libraryMoveMenu.Append(moveToBottomId , "Bottom")
        libraryMoveMenu.Append(moveToOtherId , "Other...")
        self._zoneTree.Bind(wx.EVT_MENU, self._moveToTopOfLibrary, id=moveToTopId)
        self._zoneTree.Bind(wx.EVT_MENU, self._moveToBottomOfLibrary, id=moveToBottomId)
        self._zoneTree.Bind(wx.EVT_MENU, self._moveToOtherInLibrary, id=moveToOtherId)
        return libraryMoveMenu

    def loadDeckMenu(self, event):
        try:
            deckNames = next(os.walk("decks"))[2]
    
            if deckNames == []:
                self._gamePanel.output("no decks to load")
            else:
                window = ListBoxDialog(self._gamePanel, "Loading Decks", "Choose a Deck", self._screenreader, deckNames)
                choice = window.ShowModal()
    
                if choice != -1:
                    self._gamePanel.output("loading " + deckNames[choice], True)
                    self._controller.loadDeck(deckNames[choice])
                    self._gamePanel.output("deck loaded")

                window.Destroy()

        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def autoMove(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                indicies = self._zoneTree.getIndicies()
                text = self._controller.playCardsAutoPlacement(zone, indicies) + ", from " + zone.name
                self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def moveToGraveyard(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                text = "moved "
                indicies = self._zoneTree.getIndicies()
                cards = self._controller.moveCards(zone, indicies, self._controller.player.graveyard)
    
                for card in cards:
                    text += card.cardName + ", "
    
                text = text.rstrip(", ") + " from " + zone.name + " to graveyard"
                self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def moveToExile(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                text = "moved "
                indicies = self._zoneTree.getIndicies()
                cards = self._controller.moveCards(zone, indicies, self._controller.player.exile)
    
                for card in cards:
                    text += card.cardName + ", "
    
                text = text.rstrip(", ") + " from " + zone.name + " to exile"
                self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def moveToHand(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                text = "moved "
                indicies = self._zoneTree.getIndicies()
                cards = self._controller.moveCards(zone, indicies, self._controller.player.hand)
    
                for card in cards:
                    text += card.cardName + ", "
    
                text = text.rstrip(", ") + " from " + zone.name + " to hand"
                self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def moveToLibrary(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected and not zone.isEmpty():
                self._zoneTree.PopupMenu(self._libraryMoveMenu)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def _moveToTopOfLibrary(self, event):
        try:
            currentZone = self._zoneTree.getCurrentZone()
            library = self._controller.player.library
            position = currentZone.position
            card = currentZone.remove(position)
            library.add(card, 0)
            self._gamePanel.output("Moved " + card.cardName + " from " + currentZone.name + " to the top of your library")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def _moveToBottomOfLibrary(self, event):
        try:
            currentZone = self._zoneTree.getCurrentZone()
            library = self._controller.player.library
            position = currentZone.position
            card = currentZone.remove(position)
            library.add(card, library.numberOfCards)
            self._gamePanel.output("Moved " + card.cardName + " from " + currentZone.name + " to the bottom of your  library")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def _moveToOtherInLibrary(self, event):
        try:
            currentZone = self._zoneTree.getCurrentZone()
            library = self._controller.player.library
            position = currentZone.position
            cardPositions = list(range(1, library.numberOfCards+1))
            cardPositions = list(map(str, cardPositions))
            window = ListBoxDialog(self._gamePanel, "Moving Cards to Library", "Card Position", self._screenreader, cardPositions)
            choice = window.ShowModal()
            window.Destroy()
    
            if choice != -1:
                card = currentZone.remove(position)
                library.add(card, choice)
                self._gamePanel.output("Moved " + card.cardName + " from your " + currentZone.name + " to position " + str(choice+1) + " in your library")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def getCardManaCost(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                if card.manaCost != "":
                    self._gamePanel.output(card.manaCost)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def getCardPowerAndToughness(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                if card.powerAndToughness != "":
                    self._gamePanel.output(card.powerAndToughness)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def getCardText(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                if card.text != "":
                    self._gamePanel.output(card.text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def getCardType(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                if card.type != "":
                    self._gamePanel.output(card.type)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def getCardFlavor(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                if card.flavor != "":
                    self._gamePanel.output(card.flavor)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def getCardRarity(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                if card.rarity != "":
                    self._gamePanel.output(card.rarity)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def getCardRulings(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                if card.rulings != "":
                    self._gamePanel.output(card.rulings)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def getCardPrintings(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                if card.printings != "":
                    self._gamePanel.output(card.printings)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def getCardWatermark(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                if card.watermark != "":
                    self._gamePanel.output(card.watermark)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def getCardLoyalty(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
    
                if card.loyalty != "":
                    self._gamePanel.output(card.loyalty + " loyalty")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewCard(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                cardStr = self._controller.viewCard(zone, zone.position)
                window = TextWindow(self._gamePanel, "MTG " + card.cardName, self._screenreader, cardStr)
                window.Show()
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def toggleTappedState(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()
    
            if zone is not None and self._zoneTree.cardIsSelected and zone.name.lower() != "library":
                card = zone.currentCard
    
                if card.tapped == "":
                    self._controller.tapCards(zone, (zone.position,))
                    self._gamePanel.output("Tapped " + card.cardName)
                else:
                    self._controller.untapCards(zone, (zone.position,))
                    self._gamePanel.output("Untapped " + card.cardName)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def draw(self, event):
        try:
            if not self._controller.player.library.isEmpty():
                text = self._controller.drawCards(1)
                self._gamePanel.output("Drew " + text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def drawHand(self, event):
        try:
            if not self._controller.player.library.isEmpty():
                text = self._controller.drawCards(7)
                self._gamePanel.output("Drew " + text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def shuffle(self, event):
        try:
            if not self._controller.player.library.isEmpty():
                library = self._controller.player.library
                self._controller.shuffleZone(library)
                self._gamePanel.output("Shuffled Library")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewHand(self, event):
        try:
            hand = self._controller.player.hand
            text = self._controller.viewCardNames(hand)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewVerboseHand(self, event):
        try:
            hand = self._controller.player.hand
            text = self._controller.viewCardsAndInfo(hand)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewLands(self, event):
        try:
            lands = self._controller.player.lands
            text = self._controller.viewCardNames(lands)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewVerboseLands(self, event):
        try:
            lands = self._controller.player.lands
            text = self._controller.viewCardsAndInfo(lands)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewCreatures(self, event):
        try:
            creatures = self._controller.player.creatures
            text = self._controller.viewCardNames(creatures)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewVerboseCreatures(self, event):
        try:
            creatures = self._controller.player.creatures
            text = self._controller.viewCardsAndInfo(creatures)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewOtherSpells(self, event):
        try:
            otherSpells = self._controller.player.otherSpells
            text = self._controller.viewCardNames(otherSpells)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewVerboseOtherSpells(self, event):
        try:
            otherSpells = self._controller.player.otherSpells
            text = self._controller.viewCardsAndInfo(otherSpells)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewGraveyard(self, event):
        try:
            graveyard = self._controller.player.graveyard
            text = self._controller.viewCardNames(graveyard)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewVerboseGraveyard(self, event):
        try:
            graveyard = self._controller.player.graveyard
            text = self._controller.viewCardsAndInfo(graveyard)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewExile(self, event):
        try:
            exile = self._controller.player.exile
            text = self._controller.viewCardNames(exile)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewVerboseExile(self, event):
        try:
            exile = self._controller.player.exile
            text = self._controller.viewCardsAndInfo(exile)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewLibrary(self, event):
        try:
            Library = self._controller.player.library
            text = self._controller.viewCardNames(library)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def viewVerboseLibrary(self, event):
        try:
            library = self._controller.player.library
            text = self._controller.viewCardsAndInfo(library)
            self._gamePanel.output(text)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def cleanup(self, event):
        try:
            self._controller.cleanup()
            self._gamePanel.output("Reset all zones")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def untapBattlefield(self, event):
        try:
            self._controller.untapBattlefield()
            self._gamePanel.output("untapped battlefield")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def transformCard(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()

            if zone is not None and self._zoneTree.cardIsSelected and zone.currentCard.transformation is not None and zone.name.lower() != "library":
                card = zone.currentCard
                index = zone.position
                self._gamePanel.output("transformed " + card.cardName + " into " + card.transformation.cardName)
                self._controller.transform(zone, index)
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def createToken(self, event):
        try:
            player = self._controller.player
            battlefieldZones = {"Creatures": player.creatures, "Other Spells": player.otherSpells, "Lands": player.lands}
            zoneNames = ("Creatures", "Other Spells", "Lands")
            createTokenDialog = CreateTokenDialog(self._gamePanel, "Creating Token", zoneNames, self._screenreader)
            choice = createTokenDialog.ShowModal()

            if choice != -1:
                zoneName = createTokenDialog.zoneName
                tokenCount = createTokenDialog.tokenCount
                tokenName = createTokenDialog.tokenName
                tokenType = createTokenDialog.tokenType
                tokenPower = createTokenDialog.tokenPower
                tokenToughness = createTokenDialog.tokenToughness
                tokenCardText = createTokenDialog.tokenCardText
                zone = battlefieldZones[zoneName]

                for i in range(tokenCount):
                    self._controller.createToken(zone, tokenName, tokenType, tokenPower, tokenToughness, tokenCardText)

                if tokenCount == 1:    
                    self._gamePanel.output("Created " + tokenName + ", and placed it in " + zone.name, False)
                else:
                    self._gamePanel.output("Created " + str(tokenCount) + " " + tokenName + "s, and placed them in " + zone.name, False)

            createTokenDialog.Destroy()

        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def addCounter(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()

            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                index = zone.position
                self._controller.addCounters(zone, index, 1)

                if card.counters == 1:
                    self._gamePanel.output(card.cardName + " now has " + str(card.counters) + " counter")
                else:
                    self._gamePanel.output(card.cardName + " now has " + str(card.counters) + " counters")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def subtractCounter(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()

            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                index = zone.position

                if card.counters - 1 >= 0:    
                    self._controller.subtractCounters(zone, index, 1)

                    if card.counters == 1:
                        self._gamePanel.output(card.cardName + " now has " + str(card.counters) + " counter")
                    else:
                        self._gamePanel.output(card.cardName + " now has " + str(card.counters) + " counters")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def addPlus1Counter(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()

            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                index = zone.position
                self._controller.addPlus1Counters(zone, index, 1)

                if card.plus1Counters == 1:
                    self._gamePanel.output(card.cardName + " now has " + str(card.plus1Counters) + " plus 1 counter")
                else:
                    self._gamePanel.output(card.cardName + " now has " + str(card.plus1Counters) + " plus 1 counters")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def subtractPlus1Counter(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()

            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                index = zone.position

                if card.plus1Counters - 1 >= 0:    
                    self._controller.subtractPlus1Counters(zone, index, 1)

                    if card.plus1Counters == 1:
                        self._gamePanel.output(card.cardName + " now has " + str(card.plus1Counters) + " plus 1 counter")
                    else:
                        self._gamePanel.output(card.cardName + " now has " + str(card.plus1Counters) + " plus 1 counters")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def addMinus1Counter(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()

            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                index = zone.position
                self._controller.addMinus1Counters(zone, index, 1)

                if card.minus1Counters == 1:
                    self._gamePanel.output(card.cardName + " now has " + str(card.minus1Counters) + " minus 1 counter")
                else:
                    self._gamePanel.output(card.cardName + " now has " + str(card.minus1Counters) + " minus 1 counters")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)

    def subtractMinus1Counter(self, event):
        try:
            zone = self._zoneTree.getCurrentZone()

            if zone is not None and self._zoneTree.cardIsSelected:
                card = zone.currentCard
                index = zone.position

                if card.minus1Counters - 1 >= 0:    
                    self._controller.subtractMinus1Counters(zone, index, 1)

                    if card.minus1Counters == 1:
                        self._gamePanel.output(card.cardName + " now has " + str(card.minus1Counters) + " counter")
                    else:
                        self._gamePanel.output(card.cardName + " now has " + str(card.minus1Counters) + " minus 1 counters")
        except Exception as e:
            self._gamePanel.output(e.__str__())
            self._gamePanel.log(e)