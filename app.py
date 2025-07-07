from flask import Flask, request, jsonify, render_template
import requests
import logging
import re
from logging.handlers import RotatingFileHandler
from dify_config import API_URL, API_KEY, LOG_CONFIG, HTML_ENTITIES

app = Flask(__name__)

# 配置日志记录
handler = RotatingFileHandler(
    'translation.log',
    maxBytes=LOG_CONFIG['max_bytes'],
    backupCount=LOG_CONFIG['backup_count'],
    encoding=LOG_CONFIG['encoding']
)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

def replace_html_entities(text):
    for entity, char in HTML_ENTITIES.items():
        text = text.replace(entity, char)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        app.logger.info(f"Translation request: {data['text']}")
        
        # 调用Dify API
        response = requests.post(
            API_URL,
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                "inputs": {"content": data['text']},
                "response_mode": "blocking",
                "user": "web-user"
            }
        )
        
        result = response.json()
        if response.status_code == 200:
            output = result['data']['outputs']['output']
            # 提取意译内容
            translated = re.search(r'###意译\n(.+)', output, re.DOTALL).group(1).strip()
            translated = replace_html_entities(translated)
            
            return jsonify({
                "translated": translated,
                "elapsed": result['data']['elapsed_time'],
                "tokens": result['data']['total_tokens']
            })
            
        app.logger.error(f"API Error: {result.get('error', 'Unknown error')}")
        return jsonify({"error": "Translation failed"}), 500
        
    except Exception as e:
        app.logger.error(f"Server error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
