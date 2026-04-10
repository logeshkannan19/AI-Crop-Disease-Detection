"""
ML Inference Service
====================
Handles machine learning model loading and disease prediction.
Supports multiple crops: Tomato, Potato, Corn, Wheat, Rice, Grape, Apple.
"""

import os
from pathlib import Path
from typing import Optional, Dict, List

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

from backend.app.core.config import settings
from backend.app.core.logging import logger


class DiseaseClassifier:
    """
    Plant disease classification service supporting multiple crops.
    """
    
    # All supported classes organized by crop
    CLASS_NAMES = [
        "Healthy",
        # Tomato diseases
        "Tomato_Early_Blight",
        "Tomato_Late_Blight",
        "Tomato_Leaf_Mold",
        "Tomato_Septoria_Leaf_Spot",
        "Tomato_Spider_Mites",
        "Tomato_Yellow_Curl_Virus",
        # Potato diseases
        "Potato_Early_Blight",
        "Potato_Late_Blight",
        "Potato_Common_Scab",
        "Potato_Black_Leg",
        # Corn diseases
        "Corn_Common_Rust",
        "Corn_Northern_Leaf_Blight",
        "Corn_Gray_Leaf_Spot",
        "Corn_Southern_Leaf_Blight",
        # Wheat diseases
        "Wheat_Leaf_Rust",
        "Wheat_Powdery_Mildew",
        "Wheat_Septoria_Blotch",
        # Rice diseases
        "Rice_Blast",
        "Rice_Bacterial_Leaf_Blight",
        "Rice_Sheath_Blight",
        # Grape diseases
        "Grape_Black_Rot",
        "Grape_Esca",
        "Grape_Leaf_Blight",
        # Apple diseases
        "Apple_Apple_Scab",
        "Apple_Black_Rot",
        "Apple_Cedar_Apple_Rust",
    ]

    # Treatment recommendations
    TREATMENTS: Dict[str, str] = {
        "Healthy": "Plant is healthy! Continue regular watering and monitoring. Maintain proper nutrition and ensure adequate sunlight.",
        
        # Tomato treatments
        "Tomato_Early_Blight": "Apply fungicide containing chlorothalonil or copper. Remove infected leaves immediately. Improve air circulation. Avoid overhead watering. Practice crop rotation.",
        "Tomato_Late_Blight": "Apply fungicide immediately (metalaxyl or mancozeb). Remove and destroy infected plants. Avoid overhead watering. Monitor closely as this spreads rapidly.",
        "Tomato_Leaf_Mold": "Apply fungicide containing copper or sulfur. Reduce humidity. Remove infected leaves. Improve air circulation.",
        "Tomato_Septoria_Leaf_Spot": "Apply fungicide (copper-based). Remove infected leaves. Avoid overhead watering. Practice crop rotation.",
        "Tomato_Spider_Mites": "Apply miticide. Increase humidity around plants. Remove heavily infested leaves. Use insecticidal soap.",
        "Tomato_Yellow_Curl_Virus": "Remove infected plants immediately. Control whitefly vectors with insecticide. Use resistant varieties. Prevent spread to healthy plants.",
        
        # Potato treatments
        "Potato_Early_Blight": "Apply fungicide (mancozeb or chlorothalonil). Remove infected foliage. Practice crop rotation. Use resistant varieties.",
        "Potato_Late_Blight": "Apply fungicide immediately (metalaxyl or mancozeb). Destroy infected plants. Use resistant varieties. This is a serious disease - act quickly.",
        "Potato_Common_Scab": "Maintain soil pH below 5.5. Use resistant varieties. Avoid fresh manure. Ensure consistent watering.",
        "Potato_Black_Leg": "Remove infected plants. Improve drainage. Practice crop rotation. Use certified seed potatoes.",
        
        # Corn treatments
        "Corn_Common_Rust": "Apply fungicide (triazoles). Plant resistant hybrids. Remove infected leaves. Ensure good air circulation.",
        "Corn_Northern_Leaf_Blight": "Apply fungicide at tasseling. Plant resistant hybrids. Rotate crops. Remove crop residue.",
        "Corn_Gray_Leaf_Spot": "Apply fungicide (strobilurin or triazole). Plant resistant hybrids. Rotate with non-host crops.",
        "Corn_Southern_Leaf_Blight": "Apply fungicide. Plant resistant varieties. Remove infected debris. Practice crop rotation.",
        
        # Wheat treatments
        "Wheat_Leaf_Rust": "Apply fungicide (triazoles). Plant resistant varieties. Remove infected crop residue.",
        "Wheat_Powdery_Mildew": "Apply fungicide (sulfur or triazoles). Improve air circulation. Avoid excessive nitrogen.",
        "Wheat_Septoria_Blotch": "Apply fungicide. Plant resistant varieties. Remove crop residue. Practice rotation.",
        
        # Rice treatments
        "Rice_Blast": "Apply fungicide (tricyclazole). Use resistant varieties. Avoid excessive nitrogen. Maintain proper water levels.",
        "Rice_Bacterial_Leaf_Blight": "Remove infected plants. Use resistant varieties. Avoid wounding plants. Drain fields periodically.",
        "Rice_Sheath_Blight": "Apply fungicide. Reduce plant density. Avoid excessive nitrogen. Drain fields.",
        
        # Grape treatments
        "Grape_Black_Rot": "Apply fungicide (mancozeb or myclobutanil). Remove infected parts. Improve air circulation.",
        "Grape_Esca": "No effective treatment. Remove and destroy infected vines. Prune properly. Disinfect tools.",
        "Grape_Leaf_Blight": "Apply fungicide (copper-based). Remove infected leaves. Improve air circulation.",
        
        # Apple treatments
        "Apple_Apple_Scab": "Apply fungicide (captan or myclobutanil) at bud break. Remove fallen leaves. Plant resistant varieties.",
        "Apple_Black_Rot": "Apply fungicide. Remove cankered branches. Remove mummified fruit. Practice good sanitation.",
        "Apple_Cedar_Apple_Rust": "Apply fungicide. Remove nearby cedar trees if possible. Plant resistant varieties.",
    }

    # Crop categorization
    CROPS = {
        "Tomato": {
            "icon": "🍅",
            "diseases": ["Tomato_Early_Blight", "Tomato_Late_Blight", "Tomato_Leaf_Mold", 
                        "Tomato_Septoria_Leaf_Spot", "Tomato_Spider_Mites", "Tomato_Yellow_Curl_Virus"]
        },
        "Potato": {
            "icon": "🥔",
            "diseases": ["Potato_Early_Blight", "Potato_Late_Blight", "Potato_Common_Scab", "Potato_Black_Leg"]
        },
        "Corn": {
            "icon": "🌽",
            "diseases": ["Corn_Common_Rust", "Corn_Northern_Leaf_Blight", "Corn_Gray_Leaf_Spot", "Corn_Southern_Leaf_Blight"]
        },
        "Wheat": {
            "icon": "🌾",
            "diseases": ["Wheat_Leaf_Rust", "Wheat_Powdery_Mildew", "Wheat_Septoria_Blotch"]
        },
        "Rice": {
            "icon": "🍚",
            "diseases": ["Rice_Blast", "Rice_Bacterial_Leaf_Blight", "Rice_Sheath_Blight"]
        },
        "Grape": {
            "icon": "🍇",
            "diseases": ["Grape_Black_Rot", "Grape_Esca", "Grape_Leaf_Blight"]
        },
        "Apple": {
            "icon": "🍎",
            "diseases": ["Apple_Apple_Scab", "Apple_Black_Rot", "Apple_Cedar_Apple_Rust"]
        },
        "Healthy": {
            "icon": "✅",
            "diseases": []
        }
    }

    def __init__(self):
        self.model: Optional[tf.keras.Model] = None
        self.model_loaded = False
        self.model_type = "EfficientNetB0"
        self.num_classes = len(self.CLASS_NAMES)
        self._load_model()

    def _load_model(self) -> None:
        """Load the trained model from file."""
        model_path = settings.MODEL_PATH
        
        try:
            if os.path.exists(model_path):
                self.model = load_model(model_path)
                self.model_loaded = True
                logger.info(f"Model loaded: {model_path}")
            else:
                logger.warning(f"Model not found at {model_path}. Using mock predictions.")
                self.model_loaded = False
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self.model_loaded = False

    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Load and preprocess image for prediction."""
        img = keras_image.load_img(
            image_path,
            target_size=(settings.IMAGE_SIZE, settings.IMAGE_SIZE)
        )
        img_array = keras_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
        
        return img_array

    def _detect_crop(self, disease: str) -> str:
        """Detect crop type from disease name."""
        for crop, info in self.CROPS.items():
            if disease in info["diseases"]:
                return crop
        return "Unknown"

    def predict(self, image_path: str) -> dict:
        """Predict disease from plant image."""
        if not self.model_loaded or self.model is None:
            return self._mock_prediction()

        try:
            img_array = self.preprocess_image(image_path)
            predictions = self.model.predict(img_array, verbose=0)[0]
            
            top_idx = np.argmax(predictions)
            confidence = float(predictions[top_idx])
            disease = self.CLASS_NAMES[top_idx]
            treatment = self.TREATMENTS.get(disease, "Consult an expert for treatment.")
            crop = self._detect_crop(disease)
            crop_icon = self.CROPS.get(crop, {}).get("icon", "🌱")

            top_3_indices = np.argsort(predictions)[::-1][:5]
            top_predictions = [
                {
                    "disease": self.CLASS_NAMES[idx],
                    "confidence": float(predictions[idx]),
                    "crop": self._detect_crop(self.CLASS_NAMES[idx]),
                    "crop_icon": self.CROPS.get(self._detect_crop(self.CLASS_NAMES[idx]), {}).get("icon", "🌱")
                }
                for idx in top_3_indices
            ]

            return {
                "success": True,
                "model_type": self.model_type,
                "disease": disease,
                "disease_readable": disease.replace("_", " "),
                "crop": crop,
                "crop_icon": crop_icon,
                "confidence": round(confidence * 100, 2),
                "treatment": treatment,
                "severity": self._get_severity(disease),
                "top_predictions": top_predictions
            }

        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def _get_severity(self, disease: str) -> str:
        """Get disease severity level."""
        high_severity = ["Late_Blight", "Yellow_Curl_Virus", "Black_Rot", "Blast", "Esca"]
        medium_severity = ["Early_Blight", "Rust", "Mildew", "Scab", "Blight"]
        
        for d in high_severity:
            if d in disease:
                return "High"
        for d in medium_severity:
            if d in disease:
                return "Medium"
        return "Low"

    def _mock_prediction(self) -> dict:
        """Return mock prediction when model unavailable."""
        diseases = ["Tomato_Early_Blight", "Corn_Common_Rust", "Apple_Apple_Scab", "Healthy"]
        disease = np.random.choice(diseases)
        crop = self._detect_crop(disease) if disease != "Healthy" else "Healthy"
        
        return {
            "success": True,
            "model_type": self.model_type,
            "disease": disease,
            "disease_readable": disease.replace("_", " "),
            "crop": crop,
            "crop_icon": self.CROPS.get(crop, {}).get("icon", "🌱"),
            "confidence": 85.5,
            "treatment": self.TREATMENTS.get(disease, "Consult an expert."),
            "severity": self._get_severity(disease),
            "top_predictions": [
                {"disease": disease, "confidence": 0.855, "crop": crop, "crop_icon": self.CROPS.get(crop, {}).get("icon", "🌱")},
                {"disease": "Healthy", "confidence": 0.10, "crop": "Healthy", "crop_icon": "✅"}
            ]
        }

    def get_classes(self) -> dict:
        """Get supported disease classes and treatments."""
        return {
            "model_type": self.model_type,
            "total_classes": self.num_classes,
            "classes": self.CLASS_NAMES,
            "treatments": self.TREATMENTS
        }

    def get_crops(self) -> dict:
        """Get supported crops and their diseases."""
        crops_info = []
        for crop, info in self.CROPS.items():
            if crop != "Healthy":
                diseases = []
                for d in info["diseases"]:
                    diseases.append({
                        "name": d,
                        "readable": d.replace("_", " "),
                        "severity": self._get_severity(d)
                    })
                crops_info.append({
                    "name": crop,
                    "icon": info["icon"],
                    "disease_count": len(info["diseases"]),
                    "diseases": diseases
                })
        
        return {
            "total_crops": len(crops_info),
            "total_diseases": self.num_classes - 1,
            "crops": crops_info
        }


classifier = DiseaseClassifier()


def get_classifier() -> DiseaseClassifier:
    """Get the global classifier instance."""
    return classifier
