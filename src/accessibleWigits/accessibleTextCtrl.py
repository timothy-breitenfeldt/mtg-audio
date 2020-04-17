
import wx


class AccessibleTextCtrl(wx.TextCtrl):

    def __init__(self):
        super().__init__()

    def createAccessibleTextCtrl(self, parent, name, screenreader, style=None, value=""):
        if style == None:
            self.Create(parent, value=value, name=name)
        else:
            self.Create(parent, value=value, name=name, style=style)

        self._screenreader = screenreader
        self.Bind(wx.EVT_SET_FOCUS, self.speakCTRLName)

    def speakCTRLName(self, event):
        self._screenreader.speakItem(self.GetName())

