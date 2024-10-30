from flask import Flask, render_template, request

# Import your chatbot logic (assuming it's in a separate file)
from alienbot import AlienBot

# Initialize the Flask app and your chatbot
app = Flask(__name__)
chatbot = AlienBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = chatbot.get_response(user_input)
    return {'response': response}

# Correct way to run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
