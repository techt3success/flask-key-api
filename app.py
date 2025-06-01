import os
from flask import Flask, request, jsonify
import base64


app = Flask(__name__)
DATA_FILE = 'key_store' # Path to the file where encrypted data will be stored


@app.route('/get_encrypted_data', methods=['GET'])
def get_encrypted_data():
    try:
        with open(DATA_FILE, 'rb') as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        return {'error': 'Data not found.'}, 404
    encoded_data = base64.b64encode(encrypted_data).decode()
    return {'encrypted_data': encoded_data}, 200

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
    return jsonify({'status': 'API is running'})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
