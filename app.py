from flask import Flask, request, jsonify
from datetime import datetime
from flask_caching import Cache
import os

app = Flask(__name__)

# Configure cache
app.config['CACHE_TYPE'] = 'SimpleCache'  # You can choose other cache types as needed
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout 5 minutes (for example)

cache = Cache(app)

users_db = {}
pets_db = {}
appointments_db = {}

@app.route('/user/create', methods=['POST'])
def create_user():
    user_data = request.json
    user_id = user_data['id']
    if user_id in users_db:
        return jsonify({'error': 'User already exists'}), 400
    users_db[user_id] = user_data
    # Invalidate the cache after creating a new user
    cache.delete_memoized(get_user, user_id)
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/user/<user_id>', methods=['GET'])
@cache.memoize(60)  # Cache this function for 60 seconds
def get_user(user_id):
    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@app.route('/pet/create', methods=['POST'])
def create_pet():
    pet_data = request.json
    pet_id = pet_data['id']
    if pet_id in pets_db:
        return jsonify({'error': 'Pet already exists'}), 400
    pets_db[pet_id] = pet_data
    # Invalidate the cache after creating a new pet
    cache.delete_memoized(get_pet, pet_id)
    return jsonify({'message': 'Pet created successfully'}), 201

@app.route('/pet/<pet_id>', methods=['GET'])
@cache.memoize(60)  # Cache this function for 60 seconds
def get_pet(pet_id):
    pet = pets_db.get(pet_id)
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    return jsonify(pet)

@app.route('/appointment/create', methods=['POST'])
def create_appointment():
    appointment_data = request.json
    appointment_id = str(datetime.now().timestamp())
    appointments_db[appointment_id] = appointment_data
    return jsonify({'message': 'Appointment created successfully', 'appointment_id': appointment_id}), 201

@app.route('/appointment/<appointment_id>', methods=['GET'])
@cache.memoize(60)  # Cache this function for 60 seconds
def get_appointment(appointment_id):
    appointment = appointments_db.get(appointment_id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404
    return jsonify(appointment)

@app.route('/appointment/cancel/<appointment_id>', methods=['DELETE'])
def cancel_appointment(appointment_id):
    if appointment_id in appointments_db:
        del appointments_db[appointment_id]
        # Invalidate the cache after canceling an appointment
        cache.delete_memoized(get_appointment, appointment_id)
        return jsonify({'message': 'Appointment canceled successfully'}), 200
    else:
        return jsonify({'error': 'Appointment not found to cancel'}), 404

if __name__ == '__main__':
    app.run(debug=True, host=os.getenv('FLASK_HOST', '127.0.0.1'), port=int(os.getenv('FLASK_PORT', 5000)))