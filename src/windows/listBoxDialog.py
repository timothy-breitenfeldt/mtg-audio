
import wx

from accessibleWigits import AccessibleListBox


class ListBoxDialog(wx.Dialog):

    def __init__(self, parent, dialogTitle, listBoxName, screenreader, values=[]):
        super().__init__(parent, title=dialogTitle)

        self.sizer = wx.BoxSizer()
        self._menu = AccessibleListBox()
        self._okButton = wx.Button()
        self._cancelButton = wx.Button()

        self._menu.createAccessibleListBox(self, values, wx.LB_SINGLE, listBoxName, screenreader)
        self._okButton.Create(self, wx.ID_OK, label = "ok")
        self._cancelButton.Create(self, wx.ID_CANCEL, label = "Cancel")

        self._menu.SetSelection(0)    # select the first item 
        self._okButton.SetDefault()    # Allows enter to submit the OK button if on a different ctrl.
        self.SetAffirmativeId(wx.ID_OK)
        self.SetEscapeId(wx.ID_CANCEL)
        self.sizer.Add(self._menu)
        self.sizer.Add(self._okButton)
        self.sizer.Add(self._cancelButton)
        self.SetSizer(self.sizer)
        # removes focus from the ListBox, and then refocuses the ListBox to get around a bug where it is not excepting keyDown events until focus is changed and changed back
        self._okButton.SetFocus()
        self._menu.SetFocus()

        self.Bind(wx.EVT_BUTTON, self.getCurrentSelection, self._okButton)
        self.Bind(wx.EVT_BUTTON, self.closeDialog, self._cancelButton)

    def getCurrentSelection(self, event):
        index = self._menu.GetSelection()
        self.EndModal(index)

    def closeDialog(self, event):
        self.EndModal(-1)


if __name__ == "__main__":
    pass
