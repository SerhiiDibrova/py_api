from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Animal(BaseModel):
    animal_type: str

class Cat:
    def speak(self):
        return "Meow"

class Dog:
    def speak(self):
        return "Woof"

class AnimalService:
    def __init__(self, animal_type: str):
        self.animal_type = animal_type

    def make_sound(self):
        if self.animal_type == "cat":
            return Cat().speak()
        elif self.animal_type == "dog":
            return Dog().speak()
        else:
            raise HTTPException(status_code=404, detail="Animal type not found")

@app.get("/cat/speak")
def read_cat_speak():
    animal_service = AnimalService("cat")
    return animal_service.make_sound()