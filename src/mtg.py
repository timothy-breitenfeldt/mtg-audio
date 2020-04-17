
import sys
import subprocess
import os
import time
import socket
import urllib.error

import wx

from updateUtil import UpdateUtil
from gameWindow import GameWindow
from speechUtil import SpeechUtil

class MagicTheGathering(wx.App):

    def OnInit(self):
        screenreader = SpeechUtil()
        updateUtil = UpdateUtil()

        if os.path.isdir(os.path.join(updateUtil.tempDirectory, updateUtil.updatedDirectoryName)):
            updateUtil.killProcesses(["upgrader"])
            updateUtil.removeFile("upgrader.exe")  # for windows
            updateUtil.removeFile("upgrader")  # for unix
            updateUtil.moveDirectoryContents(os.path.join(updateUtil.tempDirectory, updateUtil.updatedDirectoryName), ".")
            updateUtil.removeDirectory(os.path.join(updateUtil.tempDirectory, updateUtil.updatedDirectoryName))
        elif getattr(sys, "frozen", False):
            try:
                if not updateUtil.checkIfUpToDate() and self.showUpdateDialog():
                    updateUtil.startProcess("upgrader", os.getcwd())
                    return False
            except urllib.error.URLError:
                pass
            except urllib.error.HTTPError:
                wx.MessageBox("Unable to find server to update.", "Update         Failed", wx.OK)
            except OSError as ose:
                wx.MessageBox(str(ose), "Update         Failed", wx.OK)
            except subprocess.CalledProcessError as cpe:
                wx.MessageBox(str(cpe), "Update         Failed", wx.OK)
            except FileNotFoundError:
                wx.MessageBox(str("Try starting upgrader manually."), "Unable to start Updater", wx.OK)

        self.window = GameWindow(None, "MTG Audio")
        self.window.Show()
        return True

    def showUpdateDialog(self):
        wx.Bell()
        dialog = wx.MessageDialog(None, "There is a new update, would you like to update?", "Updater", wx.YES_NO|wx.ICON_QUESTION|wx.CANCEL)
        result = dialog.ShowModal()
        return result == wx.ID_YES


if __name__ == "__main__":
    mtg = MagicTheGathering()
    mtg.MainLoop()
