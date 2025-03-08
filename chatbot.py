from flask import Flask, render_template, request
import nltk
from nltk.tokenize import word_tokenize
import random

# Set the NLTK data path explicitly
nltk.data.path.append("C:\\Users\\oonim\\AppData\\Roaming\\nltk_data")

# Ensure the required resources are downloaded
nltk.download("punkt")

app = Flask(__name__)

# Sample responses for the chatbot
responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I help?"],
    "how are you": ["I'm just a bot, but I'm doing great! How about you?"],
    "bye": ["Goodbye!", "See you later!", "Have a great day!"],
    "default": ["I'm not sure I understand.", "Can you rephrase that?", "Tell me more!"]
}

def chatbot_response(user_input):
    """Processes user input and returns an appropriate response."""
    # Convert user input to lowercase and tokenize
    user_input = user_input.lower()
    tokens = word_tokenize(user_input)  # Tokenize the input
    
    # Check if any of the responses' keys (whole phrases) match the input
    for key in responses:
        # Create a tokenized version of the key
        key_tokens = word_tokenize(key)
        
        # Check if all tokens of the key are in the user input
        if all(token in tokens for token in key_tokens):
            return random.choice(responses[key])
    
    # Default response if no match is found
    return random.choice(responses["default"])

@app.route("/")
def home():
    """Renders the homepage."""
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    """Handles user input and returns chatbot responses."""
    user_message = request.form["msg"]
    bot_reply = chatbot_response(user_message)
    return bot_reply

if __name__ == "__main__":
    app.run(debug=True)
