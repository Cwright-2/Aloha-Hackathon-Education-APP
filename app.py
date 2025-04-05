from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from your_model import classify_cloud_image  # Replace with your model

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    file = request.files['image']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Run your model prediction here
        prediction = classify_cloud_image(filepath)

        return jsonify({'prediction': prediction})
    return jsonify({'error': 'No file uploaded'}), 400

if __name__ == '__main__':
    app.run(debug=True)
