from datetime import datetime
import pandas as pd
import os
# Get the current directory path
dir_path = os.path.dirname(os.path.realpath(__file__))
# Set the working directory to the current directory
os.chdir(dir_path)

os.chdir('../Database')

class MedicalDepartment:
    def __init__(self, name, cost_per_appointment):
        self.name = name
        self.cost_per_appointment = cost_per_appointment
        self.appointments_file = f"{name.lower()}_appointments.xlsx"

        try:
            pd.read_excel(self.appointments_file)
        except FileNotFoundError:
            pd.DataFrame(columns=["patient_id", "timestamp"]).to_excel(self.appointments_file, index=False)

    def hospitalize_patient(self, patient):
        print(f"\nPatient ID {patient.person_id} hospitalized in {self.name}.")

    def assign_doctor(self, doctor):
        self.doctor = doctor

    def reserve_appointment(self, patient, doctor_ID):
        try:
            appointments_df = pd.read_excel(self.appointments_file)
            new_appointment = pd.DataFrame({
                "patient_id": [patient.person_id],
                "timestamp": [datetime.now().strftime("%Y/%m/%d : %H:%M")],
                "doctor_id": [doctor_ID]
            })
            appointments_df = pd.concat([appointments_df, new_appointment], ignore_index=True)
            appointments_df.to_excel(self.appointments_file, index=False)
            print(f"Appointment reserved for patient ID {patient.person_id} in {self.name} department.")
        except FileNotFoundError:
            print(f"Error: Appointments file {self.appointments_file} not found.")
        except Exception as e:
            print(f"Error reserving appointment for patient ID {patient.person_id} in {self.name} department: {str(e)}")

    def delete_appointment(self, patient_id, appointments_file=None):
        if appointments_file is None:
            appointments_file = self.appointments_file

        try:
            appointments_df = pd.read_excel(appointments_file)
            appointments_df = appointments_df[appointments_df["patient_id"] != patient_id]
            appointments_df.to_excel(appointments_file, index=False)
            print(f"Appointment for patient ID {patient_id} deleted from {self.name} department.")
        except FileNotFoundError:
            print(f"Appointments file {appointments_file} not found.")
        except Exception as e:
            print(f"Error deleting appointment for patient ID {patient_id} in {self.name} department: {str(e)}")
    
    def calculate_hospitalization_cost(self, hospital):
        # Calculate the total hospitalization cost for reserved appointments
        try:
            appointments_file = pd.read_excel(f"{self.name}_appointments.xlsx")
        except FileNotFoundError:
            print(f"Error: {self.name}_appointments.xlsx not found.")
            return 0

        # Check only the "patient_id" column
        reserved_appointments = appointments_file[appointments_file['patient_id'] == hospital.patient_id]

        total_cost = len(reserved_appointments) * self.cost_per_appointment
        return total_cost
