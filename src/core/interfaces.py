from abc import ABC, abstractmethod

class IAnimal(ABC):
    """
    The IAnimal interface serves as a contract for classes representing animals.
    It declares the abstract Speak method, which must be implemented by any concrete class that implements the IAnimal interface.
    """
    @abstractmethod
    def Speak(self) -> str:
        """
        Returns a string representing the sound made by the animal.
        """
        pass