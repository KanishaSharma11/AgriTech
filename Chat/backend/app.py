import json
import random
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Load Q&A from JSON once at startup
with open(r'D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Chat\backend\chatbot_data.json') as f:
    chatbot_data = json.load(f)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get('message', '').lower()

    # Check greetings
    for greet in chatbot_data['greetings']:
        if greet.lower() in user_message:
            return jsonify({'reply': random.choice(chatbot_data['greetings'])})

    # Check farewells
    for farewell in chatbot_data['farewells']:
        if farewell.lower() in user_message:
            return jsonify({'reply': random.choice(chatbot_data['farewells'])})

    # Check Q&A matches
    for qa in chatbot_data['qas']:
        if qa['question'].lower() in user_message:
            return jsonify({'reply': qa['answer']})

    # Default response
    return jsonify({'reply': "Sorry, I didn't understand that. Please ask about weather, crops, or pests."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500, debug=True)
