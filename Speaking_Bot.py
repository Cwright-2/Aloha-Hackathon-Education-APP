"""
- Create a chatbot capable of speaking and listening to younger kids
- Add safeguards to prevent inappropriate content
- Bonus: make it as kid-friendly as possible
- Bonus: add different voices (e.g., cartoon characters)
- Bonus: enable web search functionality for additional knowledge
"""

import google.generativeai as gemnai
import requests
import re
import os
from dotenv import load_dotenv
from mainchat import start_chat

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # API key for Google services
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")  # Custom search engine ID

# Initialize gemnai for speech synthesis and recognition
gemnai.init()

# Safeguard: List of inappropriate words to filter out
# - This ensures the bot remains kid-friendly
BLOCKED_WORDS = ["violence", "hate", "danger", "inappropriate"]

# Function to filter inappropriate content
# - Checks if the response contains any blocked words
def is_safe_response(response):
    for word in BLOCKED_WORDS:
        if word in response.lower():
            return False
    return True

# Function to perform web search using Google Custom Search API
# - Allows the bot to fetch additional information from the web
def search_web(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("items", [])
        if results:
            return results[0].get("snippet", "No relevant results found.")
    return "Sorry, I couldn't find anything on that."

# Function to make the bot speak
# - Uses gemnai to convert text to speech
def speak(text, voice="default"):
    print(f"Bot: {text}")  # Debugging: Print the bot's response
    gemnai.speak(text, voice=voice)

# Function to listen to the user
# - Uses gemnai to capture audio input and convert it to text
def listen():
    print("Listening...")  # Debugging: Indicate that the bot is listening
    return gemnai.listen()

# Main chatbot loop
# - Handles the interaction between the user and the bot
def chatbot():
    convo = start_chat()  # Start the chat session from mainchat.py
    speak("Hi there! I'm your friendly speaking bot. How can I help you today?", voice="cartoon")

    while True:
        user_input = listen()  # Get user input via voice
        if not user_input:
            speak("I didn't catch that. Could you say it again?")
            continue

        # Check for inappropriate content
        if not is_safe_response(user_input):
            speak("I'm sorry, I can't talk about that.")
            continue

        # Handle web search
        if "search" in user_input.lower():
            query = re.sub(r"search", "", user_input, flags=re.IGNORECASE).strip()
            result = search_web(query)
            speak(result)
            continue

        # Send user input to the Generative AI model
        response = convo.send_message(user_input)
        bot_response = response.text

        # Check if the response is safe
        if not is_safe_response(bot_response):
            speak("I'm sorry, I can't talk about that.")
            continue

        # Speak the response
        speak(bot_response, voice="cartoon")

        # Exit condition
        if "bye" in user_input.lower():
            speak("Goodbye! Have a great day!", voice="cartoon")
            break

# Run the chatbot
if __name__ == "__main__":
    chatbot()