from flask import Flask, render_template, request, jsonify, Response
from dotenv import load_dotenv
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

        def generate():
            """Generate streaming response from Ollama"""
            stream = ollama.chat(
                model='deepseek-r1:1.5b',
                messages=[{'role': 'user', 'content': user_message}],
                stream=True,
            )
            for chunk in stream:
                response_text = chunk['message']['content'].replace("</think>", "").replace("<think>", "")
                if 'message' in chunk and 'content' in chunk['message']:
                    yield f"data: {response_text}\n\n"

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
