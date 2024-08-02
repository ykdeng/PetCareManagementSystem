from flask import Flask, request, jsonify
from datetime import datetime
from flask_caching import Cache
import os

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

cache = Cache(app)

users_db = {}
pets_db = {}
appointments_db = {}

@app.route('/user/create', methods=['POST'])
def create_user():
    try:
        user_data = request.json
        if not user_data or 'id' not in user_data:
            return jsonify({'error': 'Invalid user data'}), 400
        user_id = user_data['id']
        if user_id in users_db:
            return jsonify({'error': 'User already exists'}), 400
        users_db[user_id] = user_data
        cache.delete_memoized(get_user, user_id)
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500

@app.route('/user/<user_id>', methods=['GET'])
@cache.memoize(60)
def get_user(user_id):
    try:
        user = users_db.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500

@app.route('/pet/create', methods=['POST'])
def create_pet():
    try:
        pet_data = request.json
        if not pet_data or 'id' not in pet_data:
            return jsonify({'error': 'Invalid pet data'}), 400
        pet_id = pet_data['id']
        if pet_id in pets_db:
            return jsonify({'error': 'Pet already exists'}), 400
        pets_db[pet_id] = pet_data
        cache.delete_memoized(get_pet, pet_id)
        return jsonify({'message': 'Pet created successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500

@app.route('/pet/<pet_id>', methods=['GET'])
@cache.memoize(60)
def get_pet(pet_id):
    try:
        pet = pets_db.get(pet_id)
        if not pet:
            return jsonify({'error': 'Pet not found'}), 404
        return jsonify(pet)
    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500

@app.route('/appointment/create', methods=['POST'])
def create_appointment():
    try:
        appointment_data = request.json
        appointment_id = str(datetime.now().timestamp())
        appointments_db[appointment_id] = appointment_data
        return jsonify({'message': 'Appointment created successfully', 'appointment_id': appointment_id}), 201
    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500

@app.route('/appointment/<appointment_id>', methods=['GET'])
@cache.memoize(60)
def get_appointment(appointment_id):
    try:
        appointment = appointments_db.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        return jsonify(appointment)
    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500

@app.route('/appointment/cancel/<appointment_id>', methods=['DELETE'])
def cancel_appointment(appointment_id):
    try:
        if appointment_id in appointments_db:
            del appointments_db[appointment_id]
            cache.delete_memoized(get_appointment, appointment_id)
            return jsonify({'message': 'Appointment canceled successfully'}), 200
        else:
            return jsonify({'error': 'Appointment not found to cancel'}), 404
    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host=os.getenv('FLASK_HOST', '127.0.0.1'), port=int(os.getenv('FLASK_PORT', 5000)))