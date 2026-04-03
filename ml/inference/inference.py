"""
ML Inference Module
===================
Handles model loading and prediction for the backend API.
"""

import json
from pathlib import Path
from typing import Optional

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

# Model configuration
MODEL_PATH = Path("ml/model/plant_disease_model.keras")
MAPPING_PATH = Path("ml/model/class_mapping.json")
IMG_SIZE = 128


class InferenceEngine:
    """
    Machine learning inference engine for disease classification.
    
    Handles model loading and predictions.
    """
    
    def __init__(self, model_path: Optional[Path] = None, mapping_path: Optional[Path] = None):
        """
        Initialize the inference engine.
        
        Args:
            model_path: Path to the trained model file
            mapping_path: Path to class mapping JSON
        """
        self.model = None
        self.model_path = model_path or MODEL_PATH
        self.mapping_path = mapping_path or MAPPING_PATH
        self.classes: list[str] = []
        self.treatments: dict[str, str] = {}
        self._load_model()
        self._load_mapping()
    
    def _load_model(self) -> None:
        """Load the trained model from file."""
        if self.model_path.exists():
            try:
                self.model = load_model(str(self.model_path))
                print(f"Model loaded: {self.model_path}")
            except Exception as e:
                print(f"Warning: Could not load model: {e}")
                self.model = None
        else:
            print(f"Model file not found: {self.model_path}")
    
    def _load_mapping(self) -> None:
        """Load class names and treatments from JSON."""
        if self.mapping_path.exists():
            try:
                with open(self.mapping_path) as f:
                    data = json.load(f)
                    self.classes = data.get("classes", [])
                    self.treatments = data.get("treatments", {})
            except Exception as e:
                print(f"Warning: Could not load mapping: {e}")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for prediction.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Preprocessed image array
        """
        img = keras_image.load_img(
            image_path,
            target_size=(IMG_SIZE, IMG_SIZE)
        )
        img_array = keras_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        return img_array
    
    def predict(self, image_path: str) -> dict:
        """
        Predict disease from image.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Prediction results dictionary
        """
        if self.model is None:
            return self._mock_prediction()
        
        try:
            img_array = self.preprocess_image(image_path)
            predictions = self.model.predict(img_array, verbose=0)[0]
            
            top_idx = np.argmax(predictions)
            confidence = float(predictions[top_idx])
            disease = self.classes[top_idx] if top_idx < len(self.classes) else "Unknown"
            treatment = self.treatments.get(disease, "Consult a local agricultural expert.")
            
            # Get top 3 predictions
            top_indices = np.argsort(predictions)[::-1][:3]
            top_predictions = [
                {
                    "disease": self.classes[idx] if idx < len(self.classes) else "Unknown",
                    "confidence": float(predictions[idx])
                }
                for idx in top_indices
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
            return {
                "success": False,
                "error": str(e)
            }
    
    def _mock_prediction(self) -> dict:
        """Return mock prediction when model is unavailable."""
        return {
            "success": True,
            "disease": "Tomato_Early_Blight",
            "disease_readable": "Tomato Early Blight",
            "confidence": 85.5,
            "treatment": "Apply fungicide containing chlorothanonil or copper. Remove infected leaves. Improve air circulation.",
            "top_predictions": [
                {"disease": "Tomato_Early_Blight", "confidence": 0.855},
                {"disease": "Tomato_Late_Blight", "confidence": 0.092},
                {"disease": "Potato_Early_Blight", "confidence": 0.035}
            ]
        }
    
    def get_classes(self) -> dict:
        """Get available classes and treatments."""
        return {
            "classes": self.classes,
            "treatments": self.treatments
        }


# Global instance
inference_engine = InferenceEngine()


def get_inference_engine() -> InferenceEngine:
    """Get the global inference engine instance."""
    return inference_engine


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        result = inference_engine.predict(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python inference.py <image_path>")
        print("Or use the InferenceEngine class in your application.")