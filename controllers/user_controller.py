import requests
from os import getenv
from dotenv import load_dotenv
import json

load_dotenv()

BASE_URL = getenv('API_BASE_URL')
REGISTER_ENDPOINT = '/register'
LOGIN_ENDPOINT = '/login'
USER_DETAILS_ENDPOINT = '/user/{user_id}'

def register_user(username, password):
    url = f"{BASE_URL}{REGISTER_ENDPOINT}"
    payload = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Registration failed'}

def login_user(username, password):
    url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    payload = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Login failed'}

def get_user_details(user_id, token):
    url = BASE_URL + USER_DETAILS_ENDPOINT.format(user_id=user_id)
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Failed to fetch user details'}

if __name__ == '__main__':
    BASE_URL = 'https://example.com/api'

    register_response = register_user('username_placeholder', 'password_placeholder')
    print(register_response)

    login_response = login_user('username_placeholder', 'password_placeholder')
    print(login_response)

    user_details_response = get_user_details('user_id_placeholder', 'token_placeholder')
    print(user_details_response)