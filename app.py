from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from cloudModel import classify_cloud_image  # You write this
from dotenv import load_dotenv
from google.auth import exceptions
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Load environment variables from .env file
load_dotenv()

# Access environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Authenticate with Google Cloud
try:
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_APPLICATION_CREDENTIALS
    )
    credentials.refresh(Request())
    print("Google Cloud authentication successful.")
except (exceptions.DefaultCredentialsError, FileNotFoundError) as e:
    print(f"Google Cloud authentication failed: {e}")
    exit(1)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Call your AI model here
    prediction = classify_cloud_image(filepath)

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
