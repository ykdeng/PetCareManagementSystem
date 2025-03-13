import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_URL")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}"
}

def create_pet(pet_data):
    response = requests.post(f"{BASE_URL}/pets", json=pet_data, headers=HEADERS)
    return response.json()

def read_pet(pet_id):
    response = requests.get(f"{BASE_URL}/pets/{pet_id}", headers=HEADERS)
    return response.json()

def update_pet(pet_id, pet_data):
    response = requests.put(f"{BASE_URL}/pets/{pet_id}", json=pet_data, headers=HEADERS)
    return response.json()

def delete_pet(pet_id):
    response = requests.delete(f"{BASE_URL}/pets/{pet_id}", headers=HEADERS)
    return response.json()