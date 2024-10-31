from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def bypass_freenote(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://freenote.biz/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

@app.route('/api/freenote', methods=['GET'])
def get_freenote_content():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "fail", "message": "URL parameter is missing"}), 400

    raw_url = url.replace('freenote.biz', 'freenote.biz/raw')
    content = bypass_freenote(raw_url)
    if content:
        return jsonify({"status": "success", "content": content}), 200
    else:
        return jsonify({"status": "fail", "message": "Failed to fetch content"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
