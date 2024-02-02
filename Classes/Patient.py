from Person import Person

class Patient(Person):
    def display_info(self):
        print(f"Patient ID: {self.person_id}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}, Date of Birth: {self.date_of_birth}")