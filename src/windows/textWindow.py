
import wx

from speechUtil import SpeechUtil


class TextWindow(wx.Frame):

    def __init__(self, parent, title, screenreader, value):
        super().__init__(parent, title=title)

        self._sizer = wx.BoxSizer()
        self._screenreader = screenreader
        self._textField = wx.TextCtrl(self, value="\n" + value, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)

        self._sizer.Add(self._textField, proportion=6, flag=wx.EXPAND)
        self.SetSizer(self._sizer)
        self._textField.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

    def onKeyDown(self, event):
        if event.GetModifiers() == wx.MOD_SHIFT and event.GetKeyCode() == wx.WXK_TAB:
            self.jumpBackByCard()
        elif event.GetKeyCode() == wx.WXK_TAB:
            self.jumpForwardByCard()
        elif event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()

        event.Skip()

    def jumpForwardByCard(self):
        start = self.getLineNumber()
        lineNumber = start + 1
        totalLineCount = self._textField.GetNumberOfLines()

        if lineNumber < totalLineCount:
            while lineNumber <= totalLineCount and "------" not in self._textField.GetLineText(lineNumber):
                lineNumber += 1

            if lineNumber != start and lineNumber < self._textField.GetNumberOfLines():
                position = self._textField.XYToPosition(0, lineNumber+1)
                self._textField.SetInsertionPoint(position)
                self._screenreader.speak(self._textField.GetLineText(lineNumber+1))
            else:
                wx.Bell()
        else:
            wx.Bell()

    def jumpBackByCard(self):
        start = self.getLineNumber()
        lineNumber = start - 2

        if lineNumber >= 0:
            while lineNumber >= 0 and "------" not in self._textField.GetLineText(lineNumber):
                lineNumber -= 1

            if lineNumber != start and lineNumber > 0:
                position = self._textField.XYToPosition(0, lineNumber+1)
                self._textField.SetInsertionPoint(position)
                self._screenreader.speak(self._textField.GetLineText(lineNumber+1))
            else:
                wx.Bell()
        else:
            wx.Bell()

    def getLineNumber(self):
        position = self._textField.PositionToXY(self._textField.GetInsertionPoint())
        line = position[2]
        return line

if __name__ == "__main__":
    pass
