import requests
import os
from dotenv import load_dotenv
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

BASE_URL = os.getenv("API_URL")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}"
}

def create_pet(pet_data):
    try:
        response = requests.post(f"{BASE_URL}/pets", json=pet_data, headers=HEADERS)
        response.raise_for_status()  # Raises a HTTPError if the response was an error
        logger.info("Pet created successfully.")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error creating pet: {e}")
        return None

def read_pet(pet_id):
    try:
        response = requests.get(f"{BASE_URL}/pets/{pet_id}", headers=HEADERS)
        response.raise_for_status()
        logger.info(f"Pet details for {pet_id} retrieved successfully.")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error reading pet details for {pet_id}: {e}")
        return None

def update_pet(pet_id, pet_data):
    try:
        response = requests.put(f"{BASE_URL}/pets/{pet_id}", json=pet_data, headers=HEADERS)
        response.raise_for_status()
        logger.info(f"Pet with id {pet_id} updated successfully.")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error updating pet with id {pet_id}: {e}")
        return None

def delete_pet(pet_id):
    try:
        response = requests.delete(f"{BASE_URL}/pets/{pet_id}", headers=HEADERS)
        response.raise_for_status()
        logger.info(f"Pet with id {pet_id} deleted successfully.")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error deleting pet with id {pet_id}: {e}")
        return None

# Example of operation for testing
if __name__ == "__main__":
    pet_sample = {
        "name": "Rex",
        "type": "Dog",
        "age": 5
    }
    # Example: create a pet
    print(create_pet(pet_sample))