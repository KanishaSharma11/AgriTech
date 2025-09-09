import json
import random
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from difflib import SequenceMatcher
import string

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Load Q&A from JSON once at startup
with open(r'D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Chat\backend\chatbot_data.json') as f:
    chatbot_data = json.load(f)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

def normalize(text):
    """Lowercase and remove punctuation for loose matching."""
    return text.lower().translate(str.maketrans('', '', string.punctuation)).strip()

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = normalize(data.get('message', ''))

    # 🔹 Normalize greetings/farewells
    greetings = [normalize(g) for g in chatbot_data['greetings']]
    farewells = [normalize(f) for f in chatbot_data['farewells']]

    # 🔹 Check greetings (exact or startswith first word)
    if any(user_message == g or user_message.startswith(g.split()[0]) for g in greetings):
        return jsonify({'reply': random.choice(chatbot_data['greetings'])})

    # 🔹 Check farewells (exact or startswith first word)
    if any(user_message == f or user_message.startswith(f.split()[0]) for f in farewells):
        return jsonify({'reply': random.choice(chatbot_data['farewells'])})

    # 🔹 Fuzzy + keyword matching for Q&A
    best_match = None
    highest_score = 0
    for qa in chatbot_data['qas']:
        q_text = normalize(qa['question'])
        keyword_overlap = sum(1 for word in user_message.split() if word in q_text)
        score = similar(user_message, q_text) + (0.1 * keyword_overlap)

        if score > highest_score:
            highest_score = score
            best_match = qa

    if highest_score > 0.45:
        return jsonify({'reply': best_match['answer']})

    # 🔹 Default fallback
    return jsonify({'reply': chatbot_data.get(
        'default_answer',
        "Sorry, I don't understand that. Please ask about weather, crops, or farming technology."
    )})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500, debug=True)
