"""
ML Inference Service
=====================
Handles machine learning model loading and disease prediction.
"""

import os
from pathlib import Path
from typing import Optional

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

from backend.app.core.config import settings
from backend.app.core.logging import logger


class DiseaseClassifier:
    """
    Plant disease classification service.
    
    Handles model loading and inference for disease detection.
    """
    
    # Class names for the model
    CLASS_NAMES = [
        "Healthy",
        "Tomato_Early_Blight",
        "Tomato_Late_Blight",
        "Tomato_Leaf_Mold",
        "Potato_Early_Blight",
        "Potato_Late_Blight"
    ]

    # Treatment recommendations
    TREATMENTS = {
        "Healthy": "Plant is healthy! Continue regular watering and monitoring. Maintain proper nutrition and ensure adequate sunlight.",
        
        "Tomato_Early_Blight": "Apply fungicide containing chlorothalonil or copper. Remove infected leaves immediately. Improve air circulation around plants. Avoid overhead watering. Practice crop rotation.",
        
        "Tomato_Late_Blight": "Apply fungicide immediately (metalaxyl or mancozeb). Remove and destroy infected plants to prevent spread. Avoid overhead watering. This is a serious disease - monitor closely.",
        
        "Tomato_Leaf_Mold": "Apply fungicide containing copper or sulfur. Reduce humidity around plants. Remove infected leaves. Improve air circulation. Ensure proper spacing between plants.",
        
        "Potato_Early_Blight": "Apply fungicide (mancozeb or chlorothalonil). Remove infected foliage. Practice crop rotation. Use resistant varieties. Monitor plants regularly.",
        
        "Potato_Late_Blight": "Apply fungicide immediately (metalaxyl or mancozeb). Destroy infected plants. Use resistant varieties. Practice crop rotation. This disease can spread rapidly - act quickly."
    }

    def __init__(self):
        """Initialize the classifier and load the model."""
        self.model: Optional[Any] = None
        self.model_loaded = False
        self._load_model()

    def _load_model(self) -> None:
        """Load the trained Keras model from file."""
        model_path = settings.MODEL_PATH
        
        try:
            if os.path.exists(model_path):
                self.model = load_model(model_path)
                self.model_loaded = True
                logger.info(f"Model loaded successfully from {model_path}")
            else:
                logger.warning(f"Model file not found at {model_path}. Using mock predictions.")
                self.model_loaded = False
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self.model_loaded = False

    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Load and preprocess an image for prediction.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image as numpy array
        """
        img = keras_image.load_img(
            image_path,
            target_size=(settings.IMAGE_SIZE, settings.IMAGE_SIZE)
        )
        img_array = keras_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize to [0, 1]
        
        return img_array

    def predict(self, image_path: str) -> dict:
        """
        Predict disease from a plant leaf image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing prediction results
        """
        if not self.model_loaded or self.model is None:
            return self._mock_prediction()

        try:
            # Preprocess image
            img_array = self.preprocess_image(image_path)
            
            # Make prediction
            predictions = self.model.predict(img_array, verbose=0)[0]
            
            # Get top prediction
            top_idx = np.argmax(predictions)
            confidence = float(predictions[top_idx])
            disease = self.CLASS_NAMES[top_idx]
            treatment = self.TREATMENTS[disease]

            # Get top 3 predictions
            top_3_indices = np.argsort(predictions)[::-1][:3]
            top_predictions = [
                {
                    "disease": self.CLASS_NAMES[idx],
                    "confidence": float(predictions[idx])
                }
                for idx in top_3_indices
            ]

            return {
                "success": True,
                "disease": disease,
                "disease_readable": disease.replace("_", " "),
                "confidence": round(confidence * 100, 2),
                "treatment": treatment,
                "top_predictions": top_predictions
            }

        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def _mock_prediction(self) -> dict:
        """
        Return mock prediction when model is not available.
        
        Used for demonstration when trained model is not present.
        """
        return {
            "success": True,
            "disease": "Tomato_Early_Blight",
            "disease_readable": "Tomato Early Blight",
            "confidence": 85.5,
            "treatment": "Apply fungicide containing chlorothalonil or copper. Remove infected leaves immediately. Improve air circulation around plants.",
            "top_predictions": [
                {"disease": "Tomato_Early_Blight", "confidence": 0.855},
                {"disease": "Tomato_Late_Blight", "confidence": 0.092},
                {"disease": "Potato_Early_Blight", "confidence": 0.035}
            ]
        }

    def get_classes(self) -> dict:
        """Get list of supported disease classes and treatments."""
        return {
            "classes": self.CLASS_NAMES,
            "treatments": self.TREATMENTS
        }


# Global classifier instance
classifier = DiseaseClassifier()


def get_classifier() -> DiseaseClassifier:
    """Get the global classifier instance."""
    return classifier