from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
# from ollama import chat
import ollama
# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chatFunction():
    try:
        user_message = request.json['message']
        print('User message:', user_message)
        
        model_name = os.getenv('MODEL_NAME')

        # Get the AI response
        stream = ollama.chat(
            model='deepseek-r1:1.5b',
            messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
            stream=True,
        )
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
        return jsonify({'response': "response"})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
