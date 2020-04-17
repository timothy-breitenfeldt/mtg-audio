
import wx


class AccessibleListBox(wx.ListBox):

    def __init__(self):
        super().__init__()

    def createAccessibleListBox(self, parent, choices, style, name, screenreader):
        self.Create(parent, choices=choices, style=style, name=name)
        self._screenreader = screenreader
        self.Bind(wx.EVT_SET_FOCUS, self.speakCTRLName)

    def speakCTRLName(self, event):
        self._screenreader.speakItem(self.GetName())

