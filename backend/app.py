# Flask Backend for AI Crop Disease Detection
# ============================================
# API for plant disease classification

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.inference import predict_disease

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'backend/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Health check endpoint."""
    return jsonify({
        'status': 'running',
        'message': 'AI Crop Disease Detection API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'predict': '/api/predict (POST)'
        }
    })


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': True
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict disease from uploaded image.
    
    Expected: POST request with 'image' field containing image file.
    Returns: JSON with disease name, confidence, and treatment.
    """
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, bmp, webp'
            }), 400
        
        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save uploaded file
        file.save(filepath)
        
        # Make prediction
        result = predict_disease(filepath)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/classes', methods=['GET'])
def get_classes():
    """Get list of supported disease classes."""
    from model.inference import classifier
    
    return jsonify({
        'classes': classifier.class_names,
        'treatments': classifier.treatments
    })


if __name__ == '__main__':
    print("="*60)
    print("Starting AI Crop Disease Detection Backend...")
    print("="*60)
    app.run(host='0.0.0.0', port=5000, debug=True)