
import wx

from accessibleWigits.accessibleListBox import AccessibleListBox


class ZoneTree(AccessibleListBox):

    def __init__(self):
        super().__init__()


    def createZoneTree(self, parent, zoneOptions, zones, name, screenreader):
        self.createAccessibleListBox(parent, zoneOptions, wx.LB_SINGLE, name, screenreader)

        self._zoneOptions = zoneOptions
        self._zones = zones
        self._zoneIndex = 0
        self._screenreader = screenreader
        self._cardIsSelected = False

        for index in range(0, len(zoneOptions)):
            self.SetString(index, self.GetString(index) + " " + str(0))

        self.Bind(wx.EVT_KEY_DOWN, self.onKeydown)

    def onKeydown(self, event):
        if event.GetModifiers() == wx.MOD_CONTROL and event.GetKeyCode() == wx.WXK_RIGHT and not self._zones[self._zoneIndex].isEmpty():
            zone = self._zones[self._zoneIndex]
            zone.position = zone.numberOfCards - 1
            self.speakCard(zone.currentCard)
            self._cardIsSelected = True
        elif event.GetModifiers() == wx.MOD_CONTROL and event.GetKeyCode() == wx.WXK_LEFT and not self._zones[self._zoneIndex].isEmpty():
            zone = self._zones[self._zoneIndex]
            zone.position = 0
            self.speakCard(zone.currentCard)
            self._cardIsSelected = True
        elif event.GetKeyCode() == wx.WXK_RIGHT and not self._zones[self._zoneIndex].isEmpty():
            zone = self._zones[self._zoneIndex]
            card = zone.currentCard

            if self._cardIsSelected:
                card = zone.next()

            if card is not None:
                self.speakCard(card)

            self._cardIsSelected = True
        elif event.GetKeyCode() == wx.WXK_LEFT and not self._zones[self._zoneIndex].isEmpty():
            zone = self._zones[self._zoneIndex]
            card = zone.currentCard

            if self._cardIsSelected:
                card = zone.previous()

            if card is not None:
                self.speakCard(card)

            self._cardIsSelected = True
        elif event.GetKeyCode() == wx.WXK_DOWN:
            if (self._zoneIndex + 1) < self.GetCount():
                self._zoneIndex += 1
                zone = self._zones[self._zoneIndex]
                self.SetString(self._zoneIndex, self._zoneOptions[self._zoneIndex] + " " + str(zone.numberOfCards))
                self.SetSelection(self._zoneIndex)
                self._cardIsSelected = False

                if self.GetString(self._zoneIndex).startswith("library"):
                    zone.resetPosition()

        elif event.GetKeyCode() == wx.WXK_UP:
            if (self._zoneIndex -  1) >= 0:
                self._zoneIndex -= 1
                zone = self._zones[self._zoneIndex]
                self.SetString(self._zoneIndex, self._zoneOptions[self._zoneIndex] + " " + str(zone.numberOfCards))
                self.SetSelection(self._zoneIndex)
                self._cardIsSelected = False

                if self.GetString(self._zoneIndex) == "library":
                    zone.resetPosition()

        elif event.GetKeyCode() == wx.WXK_END:
            self._zoneIndex = len(self._zoneOptions) - 1
            self.SetString(self._zoneIndex, self._zoneOptions[self._zoneIndex] + " " + str(self._zones[self._zoneIndex].numberOfCards))
            self.SetSelection(self._zoneIndex)
            self._cardIsSelected = False
        elif event.GetKeyCode() == wx.WXK_HOME:
            self._zoneIndex = 0
            self.SetString(self._zoneIndex, self._zoneOptions[self._zoneIndex] + " " + str(self._zones[self._zoneIndex].numberOfCards))
            self.SetSelection(self._zoneIndex)
            self._cardIsSelected = False
        elif event.GetKeyCode() >= ord("A") and event.GetKeyCode() <= ord("Z"):
            self.jumpToZone(event.GetKeyCode())
            self._cardIsSelected = False

    def speakCard(self, card):
        zone = self.getCurrentZone()
        text = zone.getCardName()
        self._screenreader.speakItem(text)

    def jumpToZone(self, keyCode):
        c = chr(keyCode)
        index = self._zoneIndex + 1
        end = len(self._zoneOptions)

        # Circularly compare the given letter to the first letter of each zone by starting at the selected zone and ending at the selected zone.
        while index == len(self._zoneOptions) or (self._zoneOptions[index][0].lower() != c.lower() and index < end):
            if index == len(self._zoneOptions):
                index = 0 
                end = self._zoneIndex

            index += 1

        self._zoneIndex = index 
        self.SetString(self._zoneIndex, self._zoneOptions[self._zoneIndex] + " " + str(self._zones[self._zoneIndex].numberOfCards))
        self.SetSelection(index)

    def getCurrentCard(self):
        zone = self.getCurrentZone()
        return zone.currentCard

    def getCurrentZone(self):
        return self._zones[self._zoneIndex]

    def getIndicies(self):
        return [self._zones[self._zoneIndex].position]

    def getCurrentItem(self):
        return self.GetSelection()

    @property
    def zones(self):
        return self._zones

    @property
    def zoneOptions(self):
        return self._zoneOptions

    @property
    def cardIsSelected(self):
        return self._cardIsSelected

