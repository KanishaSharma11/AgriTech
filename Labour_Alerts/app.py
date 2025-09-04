# # from flask import Flask, render_template, request, jsonify
# # from flask_cors import CORS
# # import datetime, re

# # app = Flask(__name__)
# # CORS(app)

# # labour_posts = []

# # def sanitize(text, limit=200):
# #     return re.sub(r'[<>\'"]', '', text)[:limit].strip()

# # @app.route('/')
# # def home():
# #     return render_template('labour.html')

# # @app.route('/post-labour', methods=['POST'])
# # def post_labour():
# #     data = request.get_json() or {}
# #     required = ['work_type','number','date_needed','duration','village','taluka']
# #     if any(not data.get(k) for k in required):
# #         return jsonify({'error': 'Missing required fields'}), 400

# #     sanitized = {k: sanitize(str(data[k])) for k in data}
# #     sanitized['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #     labour_posts.append(sanitized)
# #     return jsonify({'status':'success'}), 201

# # @app.route('/labour-posts', methods=['GET'])
# # def get_labour():
# #     return jsonify(labour_posts)

# # if __name__ == '__main__':
# #     app.run(debug=True, port=5012)

# import os
# import time
# import re
# import datetime
# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# import requests
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# labour_posts = []
# news_cache = {}
# CACHE_DURATION = 300  # seconds

# def sanitize(text, limit=200):
#     return re.sub(r"[<>'\"]", "", text)[:limit].strip()

# @app.route('/')
# def dashboard():
#     return render_template('labour.html')

# @app.route('/post-labour', methods=['POST'])
# def post_labour():
#     data = request.get_json() or {}
#     required = ['work_type', 'number', 'date_needed', 'duration', 'village', 'taluka']
#     if any(not data.get(k) for k in required):
#         return jsonify({'error': 'Missing required fields'}), 400

#     entry = {k: sanitize(str(data[k])) for k in required}
#     entry['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     labour_posts.append(entry)
#     return jsonify({'status': 'success'}), 201

# @app.route('/labour-posts')
# def get_labour_posts():
#     return jsonify(labour_posts)

# @app.route('/news')
# def get_news():
#     current = time.time()
#     if 'data' in news_cache and (current - news_cache['ts']) < CACHE_DURATION:
#         return jsonify(news_cache['data'])

#     api_key = os.getenv('NEWSDATA_API_KEY')
#     if not api_key:
#         return jsonify({'error': 'API key not found'}), 500

#     api_url = 'https://newsdata.io/api/1/latest'
#     params = {
#         'apikey': 'pub_fdedca7b4b5046559819a6f4873f8e6f',
#         'q': 'farming',
#         'language': 'en',
#         'country': 'in'
#     }
#     resp = requests.get(api_url, params=params, timeout=10)

#     if resp.ok:
#         data = resp.json()
#         news_cache['data'] = data
#         news_cache['ts'] = current
#         return jsonify(data)
#     else:
#         return jsonify({'error': 'Failed to fetch news'}), resp.status_code

# if __name__ == '__main__':
#     app.run(debug=True, port=5012)


import os, time, re, datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

labour_posts = []
alerts = ["System operating normally"]
news_cache = {}
CACHE_DURATION = 300  # seconds

def sanitize(text, limit=200):
    return re.sub(r"[<>'\"]", "", text)[:limit].strip()

@app.route('/')
def dashboard():
    return render_template('labour.html')

@app.route('/post-labour', methods=['POST'])
def post_labour():
    data = request.get_json() or {}
    required = ['work_type','number','date_needed','duration','village','taluka']
    if any(not data.get(k) for k in required):
        return jsonify({'error':'Missing fields'}), 400
    entry = {k: sanitize(data[k]) for k in required}
    entry['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    labour_posts.append(entry)
    return jsonify({'status':'success'}), 201

@app.route('/labour-posts')
def get_labour_posts():
    return jsonify(labour_posts)

@app.route('/alerts')
def get_alerts():
    return jsonify(alerts)

@app.route('/news')
def get_news():
    now = time.time()
    if 'data' in news_cache and now - news_cache['ts'] < CACHE_DURATION:
        return jsonify(news_cache['data'])

    resp = requests.get('https://news.knowivate.com/api/agriculture')
    if resp.ok:
        data = resp.json()
        news_cache.update({'data': data, 'ts': now})
        return jsonify(data)
    return jsonify({'error': 'Failed to fetch news'}), resp.status_code


if __name__ == '__main__':
    app.run(debug=True, port=5012)
