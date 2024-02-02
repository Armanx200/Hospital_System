import os
import pandas as pd
from datetime import datetime

# Get the current directory path
dir_path = os.path.dirname(os.path.realpath(__file__))
# Set the working directory to the current directory
os.chdir(dir_path)

# Update the import statement for Patient
from Patient import Patient
from Doctor import Doctor

from MedicalDepartment import MedicalDepartment

os.chdir('../Database')

class Hospital:
    def __init__(self):
        # Initialize Hospital attributes
        self.departments = {
            "children": MedicalDepartment("Children", 100),
            "neurology": MedicalDepartment("Neurology", 200),
            "internal": MedicalDepartment("Internal", 300),
        }
        self.bill = 0
        self.Medicaldep = None  # Initialize Medical Department attribute
        self.patient_id = None  # Initialize patient_id attribute

    def patient_registration(self):
        # Register a new patient
        name = input("Enter patient name: ")
        age = int(input("Enter patient age: "))
        gender = input("Enter patient gender: ")
        date_of_birth = input("Enter patient date of birth (YYYY-MM-DD): ")
        patient_id = str(input("Enter patient ID: "))
        
        # Create a Patient object
        patient = Patient(name, age, gender, date_of_birth, patient_id)

        # Store patient information in "patients.xlsx"
        patients_df = pd.DataFrame({
            "name": [patient.name],
            "age": [patient.age],
            "gender": [patient.gender],
            "date_of_birth": [patient.date_of_birth],
            "patient_id": [patient.person_id],
            "date_of_registration": [datetime.now().strftime("%Y/%m/%d : %H:%M")]
        })

        try:
            existing_patients_df = pd.read_excel("patients.xlsx")
            patients_df = pd.concat([existing_patients_df, patients_df], ignore_index=True)
        except FileNotFoundError:
            pass

        patients_df.to_excel("patients.xlsx", index=False)
        print(f"Patient {patient.name} registered with ID: {patient.person_id}.")
    
    def get_specialization_input(self):
        # Ensure the user provides a valid specialization
        while True:
            specialization = input("Enter doctor specialization (children/neurology/internal): ").lower()
            if specialization in ["children", "neurology", "internal"]:
                return specialization
            else:
                print("Invalid specialization. Please enter 'children', 'neurology', or 'internal'.")

    def save_doctor_info(self):
        # Input doctor information
        name = input("Enter doctor name: ")
        age = int(input("Enter doctor age: "))
        gender = input("Enter doctor gender: ")
        date_of_birth = input("Enter doctor date of birth (YYYY-MM-DD): ")
        person_id = input("Enter doctor person ID: ")
        specialization = self.get_specialization_input()

        # Create a Doctor object
        doctor = Doctor(name, age, gender, date_of_birth, person_id, specialization)

        # Store doctor information in "doctors.xlsx"
        doctors_df = pd.DataFrame({
            "name": [doctor.name],
            "age": [doctor.age],
            "gender": [doctor.gender],
            "date_of_birth": [doctor.date_of_birth],
            "doctor_id": [doctor.person_id],
            "specialization": [doctor.specialization],
            "date_of_registration": [datetime.now().strftime("%Y/%m/%d : %H:%M")]
        })

        try:
            existing_doctors_df = pd.read_excel("doctors.xlsx")
            doctors_df = pd.concat([existing_doctors_df, doctors_df], ignore_index=True)
        except FileNotFoundError:
            pass

        doctors_df.to_excel("doctors.xlsx", index=False)
        print(f"Doctor {doctor.name} registered with ID: {doctor.person_id} and specialization: {doctor.specialization}.")


    def generate_patient_report(self, patient_id):
        # Generate a patient report with the hospitalization cost for each department
        print()
        self.bill = 0
        for department_name, department in self.departments.items():
            cost = department.calculate_hospitalization_cost(self)
            print(f"{department_name.capitalize()} Department Cost: {cost} Tomans")
            self.bill += cost

        # Add the total hospitalization cost to the patient's record in "patients.xlsx"
        try:
            patients_df = pd.read_excel("patients.xlsx")
            index = patients_df.index[patients_df['patient_id'] == patient_id].tolist()[0]
            patients_df.loc[index, 'total_cost'] = self.bill
            patients_df.to_excel("patients.xlsx", index=False)
            print(f"Total hospitalization cost added to patient ID {patient_id} in patients.xlsx")
        except Exception as e:
            print(f"Error adding total hospitalization cost to patient ID {patient_id}: {str(e)}")

    def hospital_cost_calculation(self, medical_dep):
        # Calculate the total hospitalization cost for a specific department
        self.bill = 0
        for department_name, department in self.departments.items():
            if department_name == medical_dep:
                cost = department.calculate_hospitalization_cost(self)
                self.bill += cost
        print(f"Total Hospitalization Cost: {self.bill} Tomans")

    def patient_discharge(self, medical_department_name):
        # Discharge a patient from a specific department
        medical_department = self.departments.get(medical_department_name)

        if medical_department:
            patient_id = self.patient_id

            # Update patient's total cost and create a discharge report
            self.update_patient_info_after_discharge(medical_department)

            # Delete all reservations from the appointments file
            self.delete_patient_reservations(medical_department)

            print(f"Patient ID {patient_id} discharged from {medical_department_name} department.")
        else:
            print("Invalid medical department name.")

    def delete_patient_reservations(self, medical_department):
        # Delete all reservations for the patient from the appointments file
        try:
            appointments_df = pd.read_excel(medical_department.appointments_file)
            appointments_df = appointments_df[appointments_df["patient_id"] != self.patient_id]
            appointments_df.to_excel(medical_department.appointments_file, index=False)
            print(f"All reservations for patient ID {self.patient_id} deleted.")
        except FileNotFoundError:
            print(f"Appointments file not found for {medical_department.name}.")
        except Exception as e:
            print(f"Error deleting reservations for patient ID {self.patient_id}: {str(e)}")

    def update_patient_info_after_discharge(self, medical_department):
        # Update patient's total cost and create a discharge report
        try:
            patients_df = pd.read_excel("patients.xlsx")
            index = patients_df.index[patients_df['patient_id'] == self.patient_id].tolist()[0]

            # Subtract the cost of the specific medical department
            cost_to_subtract = medical_department.calculate_hospitalization_cost(self)
            patients_df.loc[index, 'total_cost'] -= cost_to_subtract
            patients_df.to_excel("patients.xlsx", index=False)
            print(f"Total hospitalization cost updated for patient ID {self.patient_id} in patients.xlsx")

            # Create a discharge report
            discharge_report = pd.DataFrame({
                "patient_id": [self.patient_id],
                "total_cost": [cost_to_subtract],
                "time": [datetime.now().strftime("%Y/%m/%d : %H:%M")]
            })

            if os.path.exists("report.xlsx"):
                existing_report = pd.read_excel("report.xlsx")
                discharge_report = pd.concat([existing_report, discharge_report], ignore_index=True)
            discharge_report.to_excel("report.xlsx", index=False)
            print(f"Discharge report created and saved to report.xlsx")

        except Exception as e:
            print(f"Error updating total hospitalization cost or creating discharge report for patient ID {self.patient_id}: {str(e)}")
        
    def search_for_patients_by_id(self, patient_id):
        # Search for a patient by ID in the patients file
        try:
            patients_df = pd.read_excel("patients.xlsx")
            patient_data = patients_df[patients_df['patient_id'] == patient_id].iloc[0]
            print(f"Patient found: Name: {patient_data['name']}, Age: {patient_data['age']}, Gender: {patient_data['gender']}, ID: {patient_id}")
        except Exception as e:
            print(f"Patient with ID {patient_id} not found.")

    def search_for_doctors_by_id(self, doctor_id):
        # Search for a patient by ID in the patients file
        try:
            patients_df = pd.read_excel("doctors.xlsx")
            patient_data = patients_df[patients_df['doctor_id'] == doctor_id].iloc[0]
            print(f"Patient found: Name: {patient_data['name']}, Age: {patient_data['age']}, Gender: {patient_data['gender']}, ID: {doctor_id}, Department: {patient_data['specialization']}")
        except Exception as e:
            print(f"Patient with ID {doctor_id} not found.")

    def admission_of_the_patient(self):
        self.medical_dep = None  # Reset Medical Department attribute
        # Allow the user to admit a patient to a specific department
        print("\nMedical Department:")
        print("1. Children")
        print("2. Neurology")
        print("3. Internal")
        choice = input("\nEnter your choice (1-3): ")
        if choice == "1":
            self.medical_dep = "children"
        elif choice == "2":
            self.medical_dep = "neurology"
        elif choice == "3":
            self.medical_dep = "internal"
        else:
            print("Invalid choice.")
            return

        self.patient_id = input("Enter patient ID: ")
        for department_name, department in self.departments.items():
            if department_name == self.medical_dep:
                patient = Patient("Dummy Patient", 25, "Male", "1999-01-01", self.patient_id)
                department.hospitalize_patient(patient)
                self.hospital_cost_calculation(self.medical_dep)
                return
            
    
    def find_doctors_in_department(self, department):
        try:
            # Read the doctors file
            doctors_df = pd.read_excel("doctors.xlsx")

            # Filter doctors with specialization in "children"
            doctors_df = doctors_df[doctors_df["specialization"] == department]

            if not doctors_df.empty:
                # Print the details of doctors in the children department
                print(f"\nDoctors in {department} Department:")
                print(doctors_df.to_string(index=False))
            else:
                print("No doctors found in the Children Department.")
        except FileNotFoundError:
            print("Error: doctors.xlsx file not found.")

    def display_menu(self):
        # Display the menu options for the Hospital Information System
        print("\nPatient Information System Menu:")
        print("1. Patient registration")
        print("2. Reserve an appointment")
        print("3. Delete an appointment")
        print("4. Admission of the patient")
        print("5. Generate patient report")
        print("6. Patient Discharge")
        print("7. Possibility of patient search based on ID")
        print("8. Exit")

    def run(self):
        # Run the Hospital Information System and handle user input
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-8): ")

            if choice == '1':
                self.patient_registration()
            elif choice == '2':
                department_name = input("Enter department name (children, neurology, internal): ")
                if department_name in self.departments:
                    self.find_doctors_in_department(department_name)
                    doctor_ID = input("Enter Doctor ID: ")
                    department = self.departments[department_name]
                    self.patient_id = input("Enter patient ID: ")
                    patient = Patient("Dummy Patient", 25, "Male", "1999-01-01", self.patient_id)
                    department.reserve_appointment(patient, doctor_ID)
                else:
                    print("Invalid department name.")
            elif choice == '3':
                department_name = input("Enter department name (children, neurology, internal): ")
                if department_name in self.departments:
                    department = self.departments[department_name]
                    self.patient_id = input("Enter patient ID: ")
                    department.delete_appointment(self.patient_id)
                else:
                    print("Invalid department name.")
            elif choice == '4':
                self.admission_of_the_patient()
            elif choice == '5':
                self.generate_patient_report(self.patient_id)
            elif choice == '6':
                if self.medical_dep is not None:
                    self.patient_discharge(self.medical_dep)
                else:
                    print("Please admit a patient first.")
            elif choice == '7':
                patient_id = input("Enter patient ID: ")
                self.search_for_patients_by_id(patient_id)
            elif choice == '8':
                print("Exiting Hospital Patient System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
    
    def run2(self):
        while True:
            print("\nDoctor Information System Menu:")
            print("1. Doctor registration")
            print("2. Possibility of Doctor search based on ID")
            print("3. Exit")
            choice = input("\nEnter your choice (1-3): ")

            if choice == '1':
                self.save_doctor_info()
            elif choice == '2':
                doctor_id = input("Enter doctor ID: ")
                self.search_for_doctors_by_id(doctor_id)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        
            
