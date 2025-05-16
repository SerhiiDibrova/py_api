from src.core.interfaces import IAnimal
from typing import Optional

class Dog(IAnimal):
    def speak(self) -> str:
        try:
            return 'Woof!'
        except Exception as e:
            raise ValueError(f"Failed to speak: {str(e)}")

class Cat(IAnimal):
    def speak(self) -> str:
        try:
            return 'Meow!'
        except Exception as e:
            raise ValueError(f"Failed to speak: {str(e)}")

def get_animal(animal_type: str) -> Optional[IAnimal]:
    try:
        if animal_type == 'dog':
            return Dog()
        elif animal_type == 'cat':
            return Cat()
        else:
            raise ValueError('Invalid animal type')
    except Exception as e:
        raise ValueError(f"Failed to get animal: {str(e)}")