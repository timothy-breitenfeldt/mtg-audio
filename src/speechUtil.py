
from accessible_output2.outputs.auto import Auto


class SpeechUtil:

    def __init__(self, sapi=True):
        self._screenreader = Auto()
        self._history = []
        self._position = 0

    def speak(self, message):
        self._history.append(message)
        self._position = len(self._history) - 1
        self._screenreader.output(message)

    def speakItem(self, message):
        self._screenreader.output(message)

    def silence(self):
        activeScreenreader = self._screenreader.get_first_available_output()

        if activeScreenreader.name == "NVDA":
            activeScreenreader.silence()
        else:
            self._screenreader.speak(" ", interrupt=True)

    def nextSpeechHistory(self):
        historyLength = len(self._history)

        if (self._position + 1) >= historyLength :
            self.speakItem(self._history[self._position])
        else:
            self._position += 1
            self.speakItem(self._history[self._position])

    def previousSpeechHistory(self):
        historyLength = len(self._history)

        if (self._position - 1) < 0:
            self.speakItem(self._history[self._position])
        else:
            self._position -= 1
            self.speakItem(self._history[self._position])

