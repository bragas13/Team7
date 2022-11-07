from abc import ABC, abstractmethod

class State(ABC):
    
    def __init__(self, stateManager):
        self.stateManager = stateManager

    @abstractmethod
    def executeState(self):
        pass