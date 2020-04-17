
import logging

import wx

from accessibleWigits.custom import ZoneTree
from accessibleWigits.custom import CommandInputBox
from accessibleWigits.custom import CommandOutputBox
from game import GameController
from speechUtil import SpeechUtil
from gameManager import GameManager
from commandParser import CommandParser


class GamePanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        logFile = "errors.log"
        logging.basicConfig(filename=logFile, level=logging.DEBUG)

        self._controller = GameController()
        self._screenreader = SpeechUtil()
        self._zoneOptions = ("hand", "land", "creatures", "other spells", "graveyard", "exile", "library")
        self._zones = (self._controller.player.hand, self._controller.player.lands, self._controller.player.creatures, self._controller.player.otherSpells,
                self._controller.player.graveyard, self._controller.player.exile, self._controller.player.library)
        self._commandParser = CommandParser(self, self._controller, self._screenreader)
        self._zoneTree = ZoneTree()
        self._commandInput = CommandInputBox()
        self._commandOutput = CommandOutputBox()
        self._gameManager = GameManager(self, self._controller, self._zoneTree, self._screenreader)
        self._sizer = wx.BoxSizer(wx.VERTICAL)

        # Create the UI elements
        self._zoneTree.createZoneTree(self, self._zoneOptions, self._zones, "Zones", self._screenreader)
        self._commandInput.createCommandInputBox(self, wx.TE_PROCESS_ENTER, "Command:", self._screenreader, self._commandParser, self._commandOutput)
        self._commandOutput.createCommandOutputBox(self, "Output", self._screenreader)

        self._zoneTree.SetSelection(1)

        panelShortcuts = []
        zoneTreeShortcuts = []

        # Panel keyboard shortcuts
        panelShortcuts.append(self.createShortcut(wx.NewId(), (lambda event: self._screenreader.nextSpeechHistory()), keys=wx.WXK_PAGEDOWN))
        panelShortcuts.append(self.createShortcut(wx.NewId(), (lambda event: self._screenreader.previousSpeechHistory()), keys=wx.WXK_PAGEUP))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.loadDeckMenu, mods=wx.ACCEL_CTRL, keys=ord("L") ))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.createToken, mods=wx.ACCEL_CTRL, keys=ord("K") ))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.shuffle, mods=wx.ACCEL_CTRL, keys=ord("H")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.draw, mods=wx.ACCEL_CTRL, keys=ord("D")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.drawHand, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord("D")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.cleanup, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord("C")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.untapBattlefield, mods=wx.ACCEL_CTRL, keys=ord("U")))
        # view hand
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewHand, mods=wx.ACCEL_CTRL, keys=ord("1")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewVerboseHand, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord("1")))
        # view lands
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewLands, mods=wx.ACCEL_CTRL, keys=ord("2")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewVerboseLands, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord("2")))
        # view creatures
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewCreatures, mods=wx.ACCEL_CTRL, keys=ord("3")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewVerboseCreatures, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord("3")))
        # view Other Spells
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewOtherSpells, mods=wx.ACCEL_CTRL, keys=ord("4")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewVerboseOtherSpells, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord("4")))
        # view graveyard
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewGraveyard, mods=wx.ACCEL_CTRL, keys=ord("5")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewVerboseGraveyard, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord("5")))
        # view exile
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewExile, mods=wx.ACCEL_CTRL, keys=ord("6")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewVerboseExile, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord("6")))
        # view library
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewLibrary, mods=wx.ACCEL_CTRL, keys=ord("7")))
        panelShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewVerboseLibrary, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord("7")))

        # Zone Tree keyboard shortcuts
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.autoMove, keys=wx.WXK_RETURN))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.moveToGraveyard, keys=wx.WXK_BACK))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.moveToExile, mods=wx.ACCEL_SHIFT, keys=wx.WXK_BACK))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.moveToHand, mods=wx.ACCEL_SHIFT, keys=wx.WXK_RETURN))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.moveToLibrary, mods=wx.ACCEL_CTRL, keys=wx.WXK_RETURN))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.getCardManaCost, keys=ord("1")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.getCardPowerAndToughness, keys=ord("2")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.getCardText, keys=ord("3")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.getCardType, keys=ord("4")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.getCardFlavor, keys=ord("5")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.getCardRarity, keys=ord("6")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.getCardRulings, keys=ord("7")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.getCardPrintings, keys=ord("8")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.getCardWatermark, keys=ord("9")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.getCardLoyalty, keys=ord("0")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.viewCard, keys=ord("V")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.addCounter, keys=ord(">")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.subtractCounter, keys=ord("<")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.addPlus1Counter, mods=wx.ACCEL_CTRL, keys=ord(">")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.subtractPlus1Counter, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord(">")))

        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.addMinus1Counter, mods=wx.ACCEL_CTRL, keys=ord("<")))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.subtractMinus1Counter, mods=wx.ACCEL_CTRL|wx.ACCEL_SHIFT, keys=ord("<")))

        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.toggleTappedState, keys=wx.WXK_SPACE))
        zoneTreeShortcuts.append(self.createShortcut(wx.NewId(), self._gameManager.transformCard, mods=wx.ACCEL_CTRL, keys=ord("T")))

        self._panelKeyTable = wx.AcceleratorTable(panelShortcuts)
        self._zoneTreeKeyTable = wx.AcceleratorTable(zoneTreeShortcuts)
        self.SetAcceleratorTable(self._panelKeyTable)
        self._zoneTree.SetAcceleratorTable(self._zoneTreeKeyTable)
        self._sizer.Add(self._zoneTree, 1, wx.SHAPED, 0)
        self._sizer.Add(self._commandInput, 1, wx.SHAPED, 0)
        self._sizer.Add(self._commandOutput, 4, wx.EXPAND|wx.ALIGN_BOTTOM, 0)

        self._sizer.SetSizeHints(self)
        self.SetSizer(self._sizer)
        self._commandOutput.Bind(wx.EVT_KEY_DOWN, self.onKeyDownInOutput)

    def createShortcut(self, id, functionHandler, mods=0, keys=0):
        entry = wx.AcceleratorEntry(mods, keys, id)
        self.Bind(wx.EVT_MENU, functionHandler, id=id)
        return entry

    def onKeyDownInOutput(self, event):
        # append any character typed into the output box to the input box, and move the cursor to the input box
        if event.GetUnicodeKey() != 0:
            character = chr(event.GetUnicodeKey()).lower()
            self._commandInput.SetValue(self._commandInput.GetValue() + character)
            self._commandInput.SetFocus()
            self._commandInput.SetInsertionPointEnd()

        event.Skip()

    def output(self, text, interrupt=True):
        self._commandOutput.displayText(text + "\n")
        
        if interrupt:
            self._screenreader.silence()

        self._screenreader.speak(text)

    def log(self, e):
        logging.exception("\n\n" + e.__str__())
