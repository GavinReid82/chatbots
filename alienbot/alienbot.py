import re
import random

class AlienBot:
    # potential negative responses
    negative_responses = ("N", "no", "nope", "nah", "naw", "not a chance", "n", "sorry")
    # affirmative responses
    affirmative_responses = ("y", "yes", "yeah", "yup", "sure", "ok", "of course", "definitely")
    # keywords for exiting the conversation
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")
    # random starter questions about the planet
    planet_questions = (
        "What is your planet called?",
        "What kind of species live on your planet?",
        "How do you communicate on your planet?",
        "Tell me more about Earth's resources.",
        "What is the climate like on Earth?"
    )

    def __init__(self):
        self.alienbabble = {
            'describe_planet_intent': r'.*\s*your planet.*',
            'answer_why_intent': r'(W|w)hy\s(are|did).*',
            'cubed_intent': r'.*cube.*(\d+).*',
            'continue_previous_intent': r'(.*)?tell\sme\smore(\s.*)?',
            'ask_your_name_intent': r'(.*)?your\sname(.*)?',
            'ask_my_name_intent': r'(.*)?my\sname(.*)?'
        }
        self.name = None  # To store the user's name
        self.awaiting_help_response = False  # Whether the bot is waiting for a "yes" response after the greeting
        self.expecting_name = True  # Whether the bot is expecting the user's name
        self.refused_help = False  # Track if user refused to help about the planet

    def get_response(self, user_input):
        user_input = user_input.lower()

        # Handle greeting
        if self.is_greeting(user_input) and self.expecting_name and not self.name:
            return "Hello Earthling. What's your name?"

        # If the user asks for the bot's name directly
        if re.match(r"(what's|what is)\s+your\s+name", user_input):
            return self.ask_name_intent()

        # If the user asks for their own name
        if re.match(r"(what's|what is)\s+my\s+name", user_input):
            return self.ask_my_name_intent()

        # If the bot is still expecting the user's name
        if self.expecting_name and not self.name:
            return self.get_name(user_input)

        # If user has refused to help, avoid asking again
        if self.refused_help:
            return self.continue_conversation(user_input)

        # If we are waiting for a response after the greeting (yes/no), handle it
        if self.awaiting_help_response:
            return self.get_help_response(user_input)

        # Continue with the chat after the initial interactions
        return self.chat(user_input)

    def get_name(self, user_input):
        # Check if the user input is a negative response
        if user_input in self.negative_responses:
            self.reset_conversation_state(keep_name=True)
            return "Oh well, maybe next time. Have a great Earth day!"

        # Otherwise, treat the input as the user's name, but only if it's not a greeting
        if self.name is None and not self.is_greeting(user_input):
            match = re.search(r"(?:my name(?: is|'s)?|it(?:'s)?)? ?(\w+)", user_input)
            if match:
                self.name = match.group(1).capitalize()  # Store the user's response as their name
                self.awaiting_help_response = True  # Now we're waiting for the user's help response
                self.expecting_name = False  # Stop expecting name input
                return self.greet()  # Greet them after the name is provided
            else:
                return "I didn't catch your name. Could you please tell me what it is?"
        return None

    def ask_my_name_intent(self):
        # Ensure that the name is retained and returned if already known
        if self.name:
            return f"Your name is {self.name}, silly!"
        return "I don't know your name yet. What's your name?"

    def get_help_response(self, user_input):
        if self.is_affirmative(user_input):
            self.awaiting_help_response = False  # No longer waiting for a help response
            return self.ask_about_planet()  # Ask about the planet
        elif user_input in self.negative_responses:
            self.awaiting_help_response = False
            self.refused_help = True  # User refused to help, set the flag
            return "Oh well, maybe next time. Have a great Earth day!"
        else:
            return "I'm not sure what you mean. Will you help me learn about your planet?"

    def greet(self):
        # Greet only if the user has not refused help
        if not self.refused_help:
            return f"Hi {self.name}, I'm Butterball. I'm not from this planet. Will you help me learn about your planet?"
        return f"Hi {self.name}."

    # Ask about the user's planet
    def ask_about_planet(self):
        return random.choice(self.planet_questions)

    # Ask Alien's name
    def ask_name_intent(self):
        return "My name is Butterball, nice to meet you!"

    # Continue chatting without asking for help again
    def continue_conversation(self, user_input):
        return self.chat(user_input)

    # Continue chatting with the user
    def chat(self, user_input):
        if self.make_exit(user_input):
            return "Ok, have a nice Earth day!"
        
        if user_input.lower() in self.negative_responses:
            return "Fare thee well."

        response = self.match_reply(user_input.lower())
        return response

    # Check if the user wants to exit the conversation
    def make_exit(self, reply):
        for word in self.exit_commands:
            if word in reply:
                return True
        return False

    # Check if the user's input is a greeting
    def is_greeting(self, user_input):
        greeting_keywords = ("hi", "hello", "hey", "greetings", "what's up", "howdy")
        return any(keyword in user_input for keyword in greeting_keywords)

    # Check if the user's input is an affirmative response
    def is_affirmative(self, user_input):
        return any(keyword in user_input for keyword in self.affirmative_responses)

    # Match the user's input with an intent
    def match_reply(self, reply):
        for key, value in self.alienbabble.items():
            intent = key
            regex_pattern = value
            found_match = re.match(regex_pattern, reply)
            if found_match and intent == "describe_planet_intent":
                self.previous_intent = key
                return self.describe_planet_intent()
            elif found_match and intent == "answer_why_intent":
                self.previous_intent = key
                return self.answer_why_intent()
            elif found_match and intent == "cubed_intent":
                return self.cubed_intent(found_match.groups()[0])
            elif found_match and intent == "ask_your_name_intent":
                return self.ask_name_intent()
            elif found_match and intent == "ask_my_name_intent":
                return self.ask_my_name_intent()
            elif found_match and intent == "continue_previous_intent":
                if self.previous_intent == "describe_planet_intent":
                    return self.describe_planet_intent()
                elif self.previous_intent == "answer_why_intent":
                    return self.answer_why_intent()
                else:
                    return self.no_match_intent()
        return self.no_match_intent()

    def describe_planet_intent(self):
        responses = [
            "My planet is a utopia of diverse organisms and species.",
            "I am from Opidipus, the capital of the Wayward Galaxies."
        ]
        
        # Use a separate variable to track responses for this intent
        if not hasattr(self, 'used_describe_responses'):
            self.used_describe_responses = []  # Track indices of responses used by describe_planet_intent
        
        if len(self.used_describe_responses) == len(responses):
            return "That's all I feel comfortable telling you."
        
        available_responses = [i for i in range(len(responses)) if i not in self.used_describe_responses]
        selected_index = random.choice(available_responses)
        
        self.used_describe_responses.append(selected_index)
        
        return responses[selected_index]

    def answer_why_intent(self):
        responses = [
            "I come in peace.",
            "I am here to collect data on your planet and its inhabitants.",
            "I heard the coffee is good."
        ]
        
        # Use a separate variable to track responses for this intent
        if not hasattr(self, 'used_why_responses'):
            self.used_why_responses = []  # Track indices of responses used by answer_why_intent
        
        if len(self.used_why_responses) == len(responses):
            return "That's all I feel comfortable telling you."
        
        available_responses = [i for i in range(len(responses)) if i not in self.used_why_responses]
        selected_index = random.choice(available_responses)
        
        self.used_why_responses.append(selected_index)
        
        return responses[selected_index]

        
    def cubed_intent(self, number):
        number = int(number)
        cubed_number = number ** 3
        return f"The cube of {number} is {cubed_number}. Isn't that cool?"

    def no_match_intent(self):
        responses = ("Please tell me more. ", "Tell me more! ", "Why do you say that? ", "I see. Can you elaborate? ", "Interesting. Can you tell me more? ", "Why? ")
        return random.choice(responses)

    # Reset the conversation state, but ensure name is not forgotten
    def reset_conversation_state(self, keep_name=False):
        if not keep_name:
            self.name = None  # Only reset the name if explicitly told to do so
        self.awaiting_help_response = False  # No longer waiting for a help response
        if self.name is None:
            self.expecting_name = True  # Expect a name only if it hasn't been set yet
        else:
            self.expecting_name = False  # If name exists, do not reset expecting_name
