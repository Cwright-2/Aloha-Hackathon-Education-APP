import google.generativeai as gemnai
from google.generativeai import types
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import requests
import re
import os
from dotenv import load_dotenv
from google.cloud import texttospeech
import speech_recognition as sr
import time

# Set the path to your Google Cloud service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Chris/Documents/Hackathon/alohadata-team10-73d55e5fe9e7.json"

# Load environment variables from .env file
load_dotenv(dotenv_path="/Users/Chris/Documents/Hackathon/h-src/.env")

# Retrieve credentials from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")  

# Ensure the API key is loaded
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")

# Initialize gemnai for speech synthesis and recognition
gemnai.configure(api_key=GOOGLE_API_KEY)

# Google Cloud Text-to-Speech client initialization
client = texttospeech.TextToSpeechClient()

# Configure Google Generative AI (Updated for Gemini 2.0 Flash)
generation_config = {
    'temperature': 0.8,  # Controls randomness in responses
    'top_p': 0.9,        # Nucleus sampling for diversity
    'top_k': 20,         # Limits the number of highest-probability tokens
    'max_output_tokens': 2048  # Maximum length of the response
}

# Define safety settings for the model
safety_settings = [
    {
        "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
        "threshold": HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
    {
        "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        "threshold": HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
    {
        "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        "threshold": HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
    {
        "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        "threshold": HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
]

# Create a new instance of the GenerativeModel for Gemini 2.0 Flash
model = gemnai.GenerativeModel(
    model_name='gemini-2.0-flash-001',  # Updated to Gemini 2.0 Flash model
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Safeguard: List of inappropriate words to filter out
BLOCKED_WORDS = ["violence", "hate", "danger", "inappropriate"]

def is_safe_response(response):
    for word in BLOCKED_WORDS:
        if word in response.lower():
            return False
    return True

# Function to perform web search using Google Custom Search API
def search_web(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("items", [])
        if results:
            return results[0].get("snippet", "No relevant results found.")
    return "Sorry, I couldn't find anything on that."

# Function to make the bot speak using Google Cloud Text-to-Speech
def speak(text, voice="default"):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Choose voice parameters
    voice_params = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice,  # You can change the voice name based on your preferences
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Audio encoding type
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Synthesize speech
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )

    # Save the audio to a file
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

    # Optionally, you can use a library like `playsound` to play the audio file:
    # from playsound import playsound
    # playsound("output.mp3")

    print(f"Bot: {text}")  # Debugging: Print the bot's response


# Uses Google Speech Recognition to convert speech to text
# Function to listen to the user with timeout
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")  # Indicate that the bot is listening
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise

        # Listen with a timeout of 5 seconds
        try:
            audio = recognizer.listen(source, timeout=10)  # Timeout after 10 seconds if no speech is detected
            print("Recognizing...")  # Indicate that recognition is in progress
            user_input = recognizer.recognize_google(audio)  # Use Google's API for speech recognition
            print(f"You said: {user_input}")  # Debugging: Print the recognized speech
            return user_input
        except sr.WaitTimeoutError:
            print("Timeout! No speech detected.")  # If no speech detected within the timeout
            return None
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")  # In case of unclear speech
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")  # In case of API error
            return None


# Main chatbot loop
def chatbot():
    convo = model.start_chat()
    system_message = """
    You are an assistant designed to engage and support kids aged 10 and under in learning about clouds and weather in Hawai'i.
    Your goal is to provide friendly, informative, and age-appropriate responses to help children identify clouds, 
    understand weather patterns, and explore real-time weather data, including metadata like location, time, and temperature.
    Encourage curiosity and interaction with nature, motivating kids to stay active and observant of their environment. 
    Your tone should be positive, simple, and inviting, making learning fun and interactive.
    """
    convo.send_message(system_message)
    speak("Hi there! I'm sky quest. How can I help you today?", voice="en-US-Wavenet-D")


    while True:
        user_input = listen()
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
            speak("I'm sorry, I can't talk about that." )
            continue

        # Speak the response
        speak(bot_response, voice="en-US-Wavenet-D")

        # Wait to ensure the output is fully processed and saved before moving to the next question
        time.sleep(5)  # Add a small delay for saving the response


        # Exit condition (Ensure full message is spoken before exiting)
        if "bye" in user_input.lower():
            speak("Goodbye! Have a great day!", voice="en-US-Wavenet-D")
            
            # Add a small delay to ensure the full message is played before exiting
            time.sleep(10)  # Delay for 10 seconds, adjust as needed
            
            break



# Run the chatbot
if __name__ == "__main__":
    chatbot()
