
import wx

from gamePanel import GamePanel


class GameWindow(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        self.panel = GamePanel(self)
