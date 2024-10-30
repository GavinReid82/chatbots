from flask import Flask, request, jsonify
from alienbot import AlienBot  # Make sure to replace 'your_bot_file' with the actual file name where your bot resides

app = Flask(__name__)
bot = AlienBot()

@app.route("/", methods=["GET"])
def home():
    return "AlienBot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = bot.get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

