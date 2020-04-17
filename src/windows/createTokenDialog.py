
import wx
import wx.lib.intctrl

from accessibleWigits import AccessibleListBox
from accessibleWigits import AccessibleTextCtrl


class CreateTokenDialog(wx.Dialog):

    def __init__(self, parent, title, zoneNames, screenreader):
        super().__init__(parent, title=title)

        self._zoneName = ""
        self._tokenCount = 0
        self._tokenName = ""
        self._tokenType = ""
        self._tokenPower = ""
        self._tokenToughness = ""
        self._tokenCardText = ""

        self.sizer = wx.BoxSizer()
        self._zoneList = AccessibleListBox()
        self._numberOfTokensList = AccessibleListBox()
        self._tokenNameBox = AccessibleTextCtrl()
        self._tokenTypeBox = AccessibleTextCtrl()
        self._tokenPowerBox = AccessibleTextCtrl()
        self._tokenToughnessBox = AccessibleTextCtrl()
        self._tokenTextBox = AccessibleTextCtrl()
        self._okButton = wx.Button()
        self._cancelButton = wx.Button()

        listOfNumbers = tuple(range(1, 11))
        listOfNumbers = tuple(map(str, listOfNumbers))

        self._zoneList.createAccessibleListBox(self, zoneNames, wx.LB_SINGLE, "zone to create token in:", screenreader)
        self._numberOfTokensList.createAccessibleListBox(self, listOfNumbers, wx.LB_SINGLE, "how many tokens:", screenreader)
        self._tokenNameBox.createAccessibleTextCtrl(self, "token name:", screenreader, value="Token")
        self._tokenTypeBox.createAccessibleTextCtrl(self, "token type:", screenreader, value="Token")
        self._tokenPowerBox.createAccessibleTextCtrl(self, "token power:", screenreader)
        self._tokenToughnessBox.createAccessibleTextCtrl(self, "token toughness:", screenreader)
        self._tokenTextBox.createAccessibleTextCtrl(self, "token card text:", screenreader, style=wx.TE_MULTILINE)
        self._okButton.Create(self, wx.ID_OK, label = "ok")
        self._cancelButton.Create(self, wx.ID_CANCEL, label = "Cancel")

        self._zoneList.SetSelection(0)
        self._numberOfTokensList.SetSelection(0)
        self._okButton.SetDefault()    # Allows enter to submit the OK button if on a different ctrl.
        self.SetAffirmativeId(wx.ID_OK)
        self.SetEscapeId(wx.ID_CANCEL)

        self.sizer.Add(self._zoneList)
        self.sizer.Add(self._numberOfTokensList)
        self.sizer.Add(self._tokenNameBox)
        self.sizer.Add(self._tokenTypeBox)
        self.sizer.Add(self._tokenPowerBox)
        self.sizer.Add(self._tokenToughnessBox)
        self.sizer.Add(self._tokenTextBox)
        self.sizer.Add(self._okButton)
        self.sizer.Add(self._cancelButton)
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_BUTTON, self.processSuccess, self._okButton)
        self.Bind(wx.EVT_BUTTON, self.closeDialog, self._cancelButton)
        self._tokenPowerBox.Bind(wx.EVT_CHAR, self.validateIntBoxOnKeyPress)
        self._tokenToughnessBox.Bind(wx.EVT_CHAR, self.validateIntBoxOnKeyPress)

    def validateIntBoxOnKeyPress(self, event):
        key = chr(event.GetUnicodeKey())
        keyCode = event.GetKeyCode()

        if  key in "0123456789":
            event.Skip()
        elif event.IsKeyInCategory(wx.WXK_CATEGORY_NAVIGATION|wx.WXK_CATEGORY_TAB|wx.WXK_CATEGORY_CUT):
            event.Skip()
        else:
            wx.Bell()

    def processSuccess(self, event):
        self._zoneName = self._zoneList.GetString(self._zoneList.GetSelection())
        self._tokenCount = self._numberOfTokensList.GetSelection() + 1
        self._tokenName = self._tokenNameBox.GetValue().strip(" \n\r")
        self._tokenType = self._tokenTypeBox.GetValue().strip(" \n\r")
        self._tokenPower = self._tokenPowerBox.GetValue().strip(" \n\r")
        self._tokenToughness = self._tokenToughnessBox.GetValue().strip(" \n\r")
        self._tokenCardText = self._tokenTextBox.GetValue().strip(" \n\r")

        if self._tokenName == "":
            self._tokenName = "Token"
        if self._tokenType == "":
            self._tokenType = "Token"
        if self._tokenPower == "" and self._tokenToughness != "":
            self._tokenPower = "0"
        if self._tokenPower != "" and not self._tokenPower.isdigit():
            self._tokenPower = "0"
        if self._tokenToughness == "" and self._tokenPower != "":
            self._tokenToughness = "0"
        if self._tokenToughness != "" and not self._tokenToughness.isdigit():
            self._tokenToughness = "0"

        self.EndModal(1)

    def closeDialog(self, event):
        self.EndModal(-1)

    @property
    def zoneName(self):
        return self._zoneName

    @property
    def tokenCount(self):
        return self._tokenCount

    @property
    def tokenName(self):
        return self._tokenName

    @property
    def tokenType(self):
        return self._tokenType

    @property
    def tokenPower(self):
        return self._tokenPower

    @property
    def tokenToughness(self):
        return self._tokenToughness

    @property
    def tokenCardText(self):
        return self._tokenCardText
