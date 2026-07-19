from abc import ABC, abstractmethod

class Service(ABC):

    @abstractmethod
    def deposita(self, message):
        pass

    @abstractmethod
    def preleva(self):
        pass