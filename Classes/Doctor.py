import os
from Person import Person

# Get the current directory path
dir_path = os.path.dirname(os.path.realpath(__file__))
# Set the working directory to the current directory
os.chdir(dir_path)

# Class representing a doctor, inheriting from Person
class Doctor(Person):
    def __init__(self, name, age, gender, date_of_birth, person_id, specialization):
        """
        Initialize a Doctor instance.

        Inherits from:
        - Person

        Parameters:
        - name (str): The name of the doctor.
        - age (int): The age of the doctor.
        - gender (str): The gender of the doctor.
        - date_of_birth (str): The date of birth of the doctor in the format 'YYYY-MM-DD'.
        - person_id (str): The unique ID of the doctor.
        - specialization (str): The area of specialization for the doctor.
        """
        # Call the constructor of the base class (Person) with common attributes
        super().__init__(name, age, gender, date_of_birth, person_id)
        # Specific attribute for Doctor class
        self.specialization = specialization

    def display_info(self):
        """
        Display information about the doctor.
        """
        # Implementation of the abstract method to display information about the doctor
        print(f"Doctor ID: {self.person_id}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}, Date of Birth: {self.date_of_birth}, Specialization: {self.specialization}")
