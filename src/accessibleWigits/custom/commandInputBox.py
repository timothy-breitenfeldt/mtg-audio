
import shlex
import traceback

import wx

from accessibleWigits.accessibleTextCtrl import AccessibleTextCtrl


class CommandInputBox(AccessibleTextCtrl):

    def __init__(self):
        super().__init__()

    def createCommandInputBox(self, parent, style, name, screenreader, commandParser, commandOutput):
        self.createAccessibleTextCtrl(parent, name, screenreader, style)

        self._gamePanel = parent
        self._screenreader = screenreader
        self._commandParser = commandParser
        self._commandOutput = commandOutput
        self._commandStack = [""]    # stack used to repete commands, uses an empty string as a dummy head node.
        self._commandStackCapasity = 50
        self._commandCounter = 0

        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_TEXT_ENTER, self.runCommand)

    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_UP:
            if len(self._commandStack) == 1:
                wx.Bell()
            elif (self._commandCounter + 1) < len(self._commandStack):
                self._commandCounter += 1
                command = self._commandStack[self._commandCounter]
                self.SetValue(command)
            else:
                wx.Bell()
        elif event.GetKeyCode() == wx.WXK_DOWN:
            if len(self._commandStack) == 1:
                wx.Bell()
            elif (self._commandCounter - 1) >= 0:
                self._commandCounter -= 1
                command = self._commandStack[self._commandCounter]
                self.SetValue(command)
            else:
                wx.Bell()

        event.Skip()

    def _addToStack(self, command):
        if (len(self._commandStack) + 1) > (self._commandStackCapasity + 1):    # add one to the capasity to account for the dummy head node
            del self._commandStack[-1]

        self._commandStack.insert(1, command)
        self._commandCounter = 0

    def runCommand(self, event):
        command = self.GetValue()
        commandOutputText = ""

        try:
            if command != "":
                self._addToStack(command)
                command = command.lower().strip(" \t\n\r")

                # run the interface level command to clear the output window
                if command == "clear":
                    self._commandOutput.Clear()
                    self._screenreader.speak("Cleared")
                else:
                    command = shlex.split(command)
                    commandOutputText = self._commandParser.validate(command) + "\n\n"
        except Exception as e:
            commandOutputText = e.__str__()
            self._gamePanel.log(e)

        self._gamePanel.output(commandOutputText)
        self.Clear()
