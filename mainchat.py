import google.generativeai as gemnai
from google.generativeai import types
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Google Generative AI
gemnai.configure(api_key=GOOGLE_API_KEY)

# Generation configuration for the AI model
generation_config = {
    'temperature': 0.8,
    'top_p': 0.9,
    'top_k': 20,
    'max_output_tokens': 2048
}

# Define safety settings for the model
Safety_Settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
]

# Create a new instance of the GenerativeModel
model = gemnai.GenerativeModel(
    model='gemini-1.5-turbo',
    generation_config=generation_config,
    safety_settings=Safety_Settings,
)

# Function to start a chat session
def start_chat():
    convo = model.start_chat()
    system_message = """
    You are an assistant designed to engage and support kids aged 10 and under in learning about clouds and weather in Hawai'i.
    Your goal is to provide friendly, informative, and age-appropriate responses to help children identify clouds, 
    understand weather patterns, and explore real-time weather data, including metadata like location, time, and temperature.
    Encourage curiosity and interaction with nature, motivating kids to stay active and observant of their environment. 
    Your tone should be positive, simple, and inviting, making learning fun and interactive.
    """
    convo.send_message(system_message)
    return convo

# Start a new chat session
if __name__ == "__main__":
    convo = start_chat()
    while True:
        user_input = input('Gemini Prompt: ')
        convo.send_message(user_input)
        print(convo.last.text)
