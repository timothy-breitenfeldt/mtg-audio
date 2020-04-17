
import wx

from accessibleWigits.accessibleTextCtrl import AccessibleTextCtrl


class CommandOutputBox(AccessibleTextCtrl):

    def __init__(self):
        super().__init__()

    def createCommandOutputBox(self, parent, name, screenreader):
        self.createAccessibleTextCtrl(parent, name, screenreader, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)

    def displayText(self, text):
        coursorPosition = self.GetLastPosition() - 1
        self.AppendText(text)
        self.SetInsertionPoint(coursorPosition)
