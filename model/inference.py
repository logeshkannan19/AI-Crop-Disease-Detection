#!/usr/bin/env python3
"""
Plant Disease Detection - Model Inference
===========================================
This module handles model loading and prediction for the backend API.

Author: AgriTech AI Team
"""

import os
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

# Configuration
IMG_SIZE = 128
MODEL_PATH = 'model/plant_disease_model.keras'
MAPPING_PATH = 'model/class_mapping.json'

class DiseaseClassifier:
    """Handle disease classification predictions."""
    
    def __init__(self):
        """Initialize model and load class mappings."""
        self.model = None
        self.class_names = []
        self.treatments = {}
        self.class_to_index = {}
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and class mappings."""
        if os.path.exists(MODEL_PATH):
            self.model = load_model(MODEL_PATH)
            print("Model loaded successfully")
        else:
            print("Warning: Model not found. Using mock predictions.")
        
        if os.path.exists(MAPPING_PATH):
            with open(MAPPING_PATH, 'r') as f:
                mapping = json.load(f)
                self.class_names = mapping['classes']
                self.treatments = mapping['treatments']
                self.class_to_index = mapping['class_to_index']
    
    def predict(self, image_path):
        """
        Predict disease from an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            dict: Prediction result with disease name, confidence, and treatment
        """
        if self.model is None:
            return self._mock_prediction()
        
        try:
            # Load and preprocess image
            img = keras_image.load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
            img_array = keras_image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0  # Normalize
            
            # Make prediction
            predictions = self.model.predict(img_array, verbose=0)[0]
            
            # Get top prediction
            top_idx = np.argmax(predictions)
            confidence = float(predictions[top_idx])
            disease = self.class_names[top_idx] if top_idx < len(self.class_names) else "Unknown"
            
            # Get treatment
            treatment = self.treatments.get(disease, "Consult a local agricultural expert.")
            
            # Get top 3 predictions
            top_3_indices = np.argsort(predictions)[::-1][:3]
            top_3_predictions = [
                {
                    'disease': self.class_names[idx] if idx < len(self.class_names) else "Unknown",
                    'confidence': float(predictions[idx])
                }
                for idx in top_3_indices
            ]
            
            return {
                'success': True,
                'disease': disease,
                'confidence': round(confidence * 100, 2),
                'treatment': treatment,
                'top_predictions': top_3_predictions
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _mock_prediction(self):
        """Return mock prediction when model is not available."""
        return {
            'success': True,
            'disease': 'Tomato_Early_Blight',
            'confidence': 85.5,
            'treatment': 'Apply fungicide containing chlorothalonil or copper. Remove infected leaves. Improve air circulation.',
            'top_predictions': [
                {'disease': 'Tomato_Early_Blight', 'confidence': 0.855},
                {'disease': 'Tomato_Late_Blight', 'confidence': 0.092},
                {'disease': 'Potato_Early_Blight', 'confidence': 0.035}
            ]
        }


# Global classifier instance
classifier = DiseaseClassifier()


def predict_disease(image_path):
    """Convenience function for prediction."""
    return classifier.predict(image_path)


if __name__ == '__main__':
    # Test with a sample image if available
    import sys
    
    if len(sys.argv) > 1:
        result = predict_disease(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python inference.py <image_path>")