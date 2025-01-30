from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        # Prepare the request to Ollama
        ollama_url = os.getenv('OLLAMA_API_URL')
        model_name = os.getenv('MODEL_NAME')
        
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
        
        # Make request to Ollama
        response = requests.post(ollama_url, json=payload)
        
        if response.status_code == 200:
            ai_response = response.json()['message']['content']
            return jsonify({'response': ai_response})
        else:
            return jsonify({'error': 'Failed to get response from Ollama'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
