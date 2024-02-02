import os
import sys


# Get the current directory path
dir_path = os.path.dirname(os.path.realpath(__file__))
# Set the working directory to the current directory
os.chdir(dir_path)
sys.path.append('Classes/')

# Import the Hospital class from Hospital.py
from Hospital import Hospital

# Example usage
hospital_system = Hospital()

while True:
    print("\nHospital Information System Menu:")
    print("1. Patient")
    print("2. Doctor")
    print("3. Exit")
    choice = input("\nEnter your choice (1-3): ")

    if choice == '1':
        hospital_system.run()
    elif choice == '2':
        hospital_system.run2()
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 3.")
