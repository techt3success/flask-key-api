from flask import Flask, request, jsonify
import json
import os
from cryptography.fernet import Fernet


app = Flask(__name__)
DATA_FILE = 'key_store'


@app.route('/get_encrypted_data', methods=['GET'])
def get_encrypted_data():
    with open(DATA_FILE, 'rb') as f:
        encrypted_data = f.read()
    return {'encrypted_data': encrypted_data}, 200


@app.route('/save_enc_data', methods=['POST'])
def save_enc_data():
    req = request.data
    if not req:
        return {'error': 'No data provided.'}, 400
    
    # save the encrypted data to key_store file
    with open(DATA_FILE, 'wb') as f:
        f.write(req)
    return {'message': 'Data saved successfully.'}, 200

@app.route('/')
def index():
    return {'status': 'API is running'}, 200

if __name__ == '__main__':
    app.run()
