from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import datetime, re

app = Flask(__name__)
CORS(app)
posts = []

def sanitize(text, limit):
    return re.sub(r'[<>\'"]','', text)[:limit].strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forum', methods=['GET','POST'])
def forum():
    if request.method == 'POST':
        data = request.get_json() or {}
        name = sanitize(data.get('name',''), 100)
        message = sanitize(data.get('message',''), 1000)
        if not name or not message:
            return jsonify({'error': 'Invalid input'}), 400
        posts.append({'name': name, 'message': message, 'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        return jsonify({'status':'ok'}), 201
    return jsonify(posts)

if __name__ == '__main__':
    app.run(debug=True, port=5506)
