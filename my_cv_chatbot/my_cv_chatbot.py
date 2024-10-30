from flask import Flask, request, jsonify, render_template, session

my_cv_chatbot = Flask(__name__)
my_cv_chatbot.secret_key = 'supersecretkey'  # Necessary for session management

import random
import re
import csv

# Load your CSV data
with open("cv.csv", "r") as file:
    reader = csv.DictReader(file)
    data = list(reader)

basic_responses = {
    "hello": ["Hi", "Hey", "Nice to meet you"],
    "hi": ["Hi", "Hey", "Nice to meet you"],
    "how are you?": ["Fine, thanks", "I'm good, how are you?", "Less of the chit-chat, let's get started."],
    "goodbye": ["Bye!", "Check you later", "Stay cool!"]
}

@my_cv_chatbot.route('/')
def index():
    session.clear()  # Clear session at the start of a new conversation
    return render_template('index.html')

@my_cv_chatbot.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    response = session.get('response', None)  # Get the current response session
    response_index = session.get('response_index', 0)  # Get the current index

    if response is None:
        if detect_greeting(user_input):
            bot_reply = random.choice(basic_responses["hello"])
        elif user_input.lower() in basic_responses:
            bot_reply = random.choice(basic_responses[user_input.lower()])
        elif user_input.lower() in ["bye", "exit", "quit", "goodbye"]:
            bot_reply = random.choice(basic_responses["goodbye"])
        elif user_input.lower() == "help":
            bot_reply = help()
        else:
            response = regex(user_input)
            if response:
                session['response'] = response  # Store the response list in session
                session['response_index'] = 1  # Start from the first item
                bot_reply = response[0]
                bot_reply += " Would you like to hear more? (yes/no)"
            else:
                bot_reply = "I'm not sure how to respond to that. Type 'help' to see what you can ask me."
    else:
        if user_input.lower() in ["yes", "y"]:
            if response_index < len(response):
                bot_reply = response[response_index]
                response_index += 1
                if response_index < len(response):
                    bot_reply += " Would you like to hear more? (yes/no)"
                session['response_index'] = response_index  # Update the index in session
            else:
                bot_reply = "That's all the information I have."
                session.pop('response', None)  # Clear response from session
                session.pop('response_index', None)  # Clear index from session
        else:
            bot_reply = "Okay, let me know if you have any other questions."
            session.pop('response', None)  # Clear response from session
            session.pop('response_index', None)  # Clear index from session

    return jsonify({"response": bot_reply})

def detect_greeting(user):
    greetings = ["hi", "hello", "hey", "greetings"]
    for word in greetings:
        if word in user.lower():
            return True
    return False

def regex(user):
    if re.search(r"education", user, re.IGNORECASE):
        return [row['education'] for row in data if row['education']]
    elif re.search(r"(qualifications|skills)", user, re.IGNORECASE):
        return [row['qualifications'] for row in data if row['qualifications']]
    elif re.search(r"(experience|work)", user, re.IGNORECASE):
        return [row['work'] for row in data if row['work']]
    else:
        return None

def help():
    return """
    You can ask me about the following topics:
    - Education: Ask about my educational background (e.g., "Tell me about your education")
    - Qualifications: Ask about my qualifications or skills (e.g., "What qualifications do you have?")
    - Work Experience: Ask about my work experience (e.g., "Tell me about your work experience")

    You can also say:
    - "hello", "hi": To greet me
    - "how are you?": To ask how I am
    - "goodbye", "bye", "exit", "quit": To end the conversation

    Type 'help' at any time to see this message again.
    """

if __name__ == '__main__':
    my_cv_chatbot.run(debug=True)
