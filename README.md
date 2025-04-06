# 🌤️ Sky-Quest: An Interactive Cloud & Weather Learning Bot for Kids

**Sky-Quest** is a voice-enabled, AI-powered chatbot designed to help kids aged 10 and under explore clouds and weather patterns in Hawaiʻi. It’s a fun, safe, and interactive way to encourage outdoor learning, curiosity, and connection with the natural world.

---

## 📚 What It Does

- 🗣️ **Talks and Listens** – Uses speech recognition and text-to-speech to hold natural conversations with kids.
- ☁️ **Identifies Clouds and Weather** – Explains different types of clouds and what they mean for the weather.
- 🌍 **Encourages Real-World Exploration** – Promotes outdoor observation using local time, location, and temperature.
- 🔍 **Performs Web Searches** – Handles safe, filtered queries using Google Custom Search.
- ✅ **Filters Unsafe Topics** – Blocks inappropriate words and uses Gemini's content safety tools.
- 🌈 **Hawaii Context** – Localized to help kids in Hawaiʻi understand their unique environment.

---

## 🚀 Technologies Used

- **Google Gemini-2.0-flash-001 (Generative AI)** – For natural language responses.
- **Speech Recognition + Text-to-Speech** – Via custom `gemnai` module (or compatible tools like `SpeechRecognition`, `gTTS`, `pyttsx3`, etc.).
- **Google Custom Search API** – For safe and filtered web queries.
- **dotenv** – For managing API keys securely with environment variables.

---

## 🛡️ Kid-Safe Features

- Strict **Gemini Safety Settings** for filtering content.
- Custom **blocked words list** to avoid harmful topics.
- Friendly, age-appropriate responses.
- No storage of user data or personal information.


---

## 🔧 How to Run

1. **Clone the repo:**

   ```bash
   git clone https://github.com/Cwright-2/Aloha-Hackathon-Education-APP.git
   cd Aloha-Hackathon-Education-APP
