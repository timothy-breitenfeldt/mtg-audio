
from abc import ABC, abstractmethod


class IAction(ABC):

    def __init__(self):
        raise TypeError("Unable to instantiate interface.")

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def redo(self):
        pass
