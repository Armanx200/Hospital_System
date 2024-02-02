# Hospital Information System

This GitHub repository contains a Python implementation of a Hospital Information System, designed to manage patient and doctor records, appointments, hospitalizations, and reporting. The system is built using object-oriented programming principles and leverages Pandas for data manipulation, and Excel files for persistent data storage.

## Key Components

### 1. Hospital Class (`Hospital.py`)

#### Functionality
- Patient registration.
- Doctor registration.
- Admission of patients to specific departments.
- Generation of patient reports with hospitalization costs.
- Patient discharge from a specific department.
- Search for patients and doctors based on ID.

#### Dependencies
- Requires `Pandas` for data manipulation.
- Integrates with `Patient` and `Doctor` classes for managing individual records.
- Utilizes `MedicalDepartment` class for handling medical department operations.

### 2. MedicalDepartment Class (`MedicalDepartment.py`)

#### Functionality
- Represents a medical department with attributes such as name, cost per appointment, and an appointments file.
- Manages hospitalization of patients, appointment reservations, and cost calculation.

#### Dependencies
- Requires `Pandas` for data manipulation.
- Utilizes `datetime` for timestamping appointments.
- Inherits from `ABC` for abstract methods and adheres to an interface defined in the `Person` class.

### 3. Patient Class (`Patient.py`)

#### Functionality
- Represents a patient with attributes inherited from the `Person` class.
- Displays patient information.

#### Dependencies
- Inherits from the abstract `Person` class.

### 4. Doctor Class (`Doctor.py`)

#### Functionality
- Represents a doctor with attributes inherited from the `Person` class.
- Displays doctor information.

#### Dependencies
- Inherits from the abstract `Person` class.

### 5. Person Class (`Person.py`)

#### Functionality
- Abstract class defining common attributes for patients and doctors.
- Provides an abstract method for displaying information.

#### Dependencies
- Inherits from `ABC` for abstract methods.
- Utilizes `datetime` for timestamping.

### 6. Main Execution Script (`main.py`)

#### Functionality
- Handles user interaction and menu-driven execution of the hospital system.
- Utilizes the `Hospital` class for managing patient and doctor functionalities.
- Allows users to choose between patient and doctor operations or exit the system.

## Usage Instructions

1. Run the `main.py` script to initiate the Hospital Information System.
2. Choose between patient and doctor operations or exit the system using the provided menu.

## Note

Ensure that the necessary dependencies (`Pandas`, `datetime`) are installed before running the system.
