# 🌤️ Sky-Quest — Aloha Hackathon Education App

**Sky-Quest** is a fun, voice-enabled educational chatbot designed for kids 10 and under to explore clouds and weather in Hawai‘i. Created for the **Aloha Hackathon**, this app combines speech recognition, AI-generated responses from Google Gemini, and child-friendly text-to-speech feedback to create an engaging learning experience.

---

## 🧠 What It Does

Sky-Quest encourages curiosity and learning by helping kids:

- Identify cloud types and their meanings
- Understand weather patterns through interactive conversation
- Explore and engage with their environment in a mindful, educational way

---

## 🧩 Features

- 🎙️ **Voice Interaction**: Ask questions and get spoken responses
- ☁️ **Gemini-Powered Responses**: AI-generated answers tailored for children
- 🔍 **Safe Search**: Integrated Google Custom Search for safe, relevant information
- 🗣️ **Google Cloud TTS**: Realistic, child-friendly speech feedback
- 🔐 **Content Safety**: Filters out inappropriate topics and language

---

## 🛠️ Built With

- **Python 3.8+**
- Google Generative AI (Gemini)
- Google Cloud Text-to-Speech
- SpeechRecognition
- Google Custom Search API
- dotenv for environment variable management

---

## 🚀 Getting Started

Follow these steps to get Sky-Quest up and running on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Aloha-Hackathon-Education-APP.git
cd Aloha-Hackathon-Education-APP
```

### 2. Set Up API Keys and Environment Variables

Create a `.env` file in the root directory and add your credentials:

```ini
GOOGLE_API_KEY=your_google_api_key
SEARCH_ENGINE_ID=your_custom_search_engine_id
```

Also, set your Google Cloud service account key either in the script or through the terminal:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
```

*Tip: Add this line to your shell’s startup script (e.g., `.bashrc`, `.zshrc`) for persistence.*

### 3. Install Dependencies

Install the required packages with pip:

```bash
pip install -r requirements.txt
```

*Sample `requirements.txt`:*

```txt
google-generativeai
google-cloud-texttospeech
SpeechRecognition
python-dotenv
requests
```

### 4. Run the App

Launch the chatbot with:

```bash
python Integrated_Chatbot.py
```

Sky-Quest will greet you and begin listening for your questions!

---

## 🧠 Example Conversations

**Kid:** What kind of cloud is fluffy and white?  
**Sky-Quest:** That’s a cumulus cloud—it looks like a big cotton ball and usually means good weather!

**Kid:** What do dark clouds mean?  
**Sky-Quest:** Dark clouds like nimbostratus often bring rain, so you might want to grab your umbrella!

---

## 📁 Project Structure

| File                        | Purpose                                                   |
|-----------------------------|-----------------------------------------------------------|
| `Integrated_Chatbot.py`      | Main chatbot with speech input/output and Gemini AI        |
| `cloudModel.py`              | (Optional) Logic for classifying or identifying clouds    |
| `app.py`                     | (Optional) Web/backend interface for the app              |

---

## 💡 Future Features

- 📷 Cloud image classification
- 📍 Weather tracking with GPS and time metadata
- 🏅 Missions and achievements for nature exploration
- 📴 Offline voice model support

---

## 🧒 Child Safety First

Sky-Quest is designed with safety in mind:

- No harmful or adult content
- Uses trusted, verified sources for all information
- Encourages learning while preventing screen addiction

---

Now you're ready to help kids learn about clouds and weather in Hawai‘i with Sky-Quest!
```
