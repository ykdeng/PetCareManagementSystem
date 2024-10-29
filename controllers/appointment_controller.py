import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('API_BASE_URL')

def create_appointment(data):
    response = requests.post(f"{BASE_URL}/appointments", json=data)
    return response.json()

def get_appointments():
    response = requests.get(f"{BASE_URL}/appointments")
    return response.json()

def get_appointment_by_id(appointment_id):
    response = requests.get(f"{BASE_URL}/appointments/{appointment_id}")
    return response.json()

def update_appointment(appointment_id, data):
    response = requests.put(f"{BASE_URL}/appointments/{appointment_id}", json=data)
    return response.json()

def delete_appointment(appointment_id):
    response = requests.delete(f"{BASE_URL}/appointments/{appointment_id}")
    return response.status_code == 204

if __name__ == "__main__":
    new_appointment_data = {
        "pet_name": "Charlie",
        "appointment_date": "2023-10-05",
        "reason": "Annual Checkup"
    }
    print("Creating an appointment...", create_appointment(new_appointment_data))

    print("Fetching list of appointments...", get_appointments())

    appointment_id_to_update = 1
    update_data = {"reason": "Vaccination"}
    print(f"Updating appointment {appointment_id_to_update}...", update_appointment(appointment_id_to_update, update_data))

    appointment_id_to_delete = 1
    print(f"Deleting appointment {appointment_id_to_delete}...", delete_appointment(appointment_id_to_delete))