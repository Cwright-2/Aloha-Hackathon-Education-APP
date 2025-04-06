from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import random

from cloudModel import classify_cloud_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CLOUD_TYPES = ['cumulonimbus', 'cumulus', 'stratus', 'cirrus', 'nimbostratus', 'altocumulus', 'stratocumulus', 'cirrostratus', 'cirrocumulus', 'stratiformis']

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

    # Temporarily generate a random cloud type
    # prediction = random.choice(CLOUD_TYPES)

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
