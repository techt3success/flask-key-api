from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'
ENCRYPTED_DATA = "key_store"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/encrypted_data', methods=['GET'])
def get_encrypted_data():
    with open(ENCRYPTED_DATA, 'r') as f:
        encrypted_data = f.read()
    return {'encrypted_data': encrypted_data}, 200

@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    data = load_data()
    if key in data:
        return {'key': key, 'value': data[key]}, 200
    else:
        return {'message': f'Key "{key}" not found. Please provide a value.'}, 404

@app.route('/set', methods=['POST'])
def set_value():
    req = request.get_json()
    key = req.get('key')
    value = req.get('value')
    if not key or value is None:
        return {'error': 'Both "key" and "value" must be provided.'}, 400

    data = load_data()
    data[key] = value
    save_data(data)
    return {'message': f'Saved: {key} = {value}'}, 200

@app.route('/')
def index():
    return {'status': 'API is running'}, 200

if __name__ == '__main__':
    app.run()
