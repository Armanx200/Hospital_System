from abc import ABC, abstractmethod
from datetime import datetime

class Person(ABC):
    def __init__(self, name, age, gender, date_of_birth, person_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.person_id = person_id
        self.timestamp = datetime.now().strftime("%Y/%m/%d : %H:%M")

    @abstractmethod
    def display_info(self):
        pass