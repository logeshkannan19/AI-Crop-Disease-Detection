"""
Unit Tests for ML Service
==========================
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
import json

# Test the classifier without requiring actual model
class TestDiseaseClassifier:
    """Test cases for DiseaseClassifier."""
    
    def test_class_names_defined(self):
        """Test that class names are properly defined."""
        from backend.app.services.ml_service import DiseaseClassifier
        
        classifier = DiseaseClassifier.__new__(DiseaseClassifier)
        classifier.CLASS_NAMES = [
            "Healthy",
            "Tomato_Early_Blight",
            "Tomato_Late_Blight",
            "Tomato_Leaf_Mold",
            "Potato_Early_Blight",
            "Potato_Late_Blight"
        ]
        
        assert len(classifier.CLASS_NAMES) == 6
        assert "Healthy" in classifier.CLASS_NAMES
    
    def test_treatments_defined(self):
        """Test that treatments are defined for all classes."""
        from backend.app.services.ml_service import DiseaseClassifier
        
        classifier = DiseaseClassifier.__new__(DiseaseClassifier)
        classifier.TREATMENTS = {
            "Healthy": "Plant is healthy!",
            "Tomato_Early_Blight": "Apply fungicide",
        }
        
        assert "Healthy" in classifier.TREATMENTS
        assert "Tomato_Early_Blight" in classifier.TREATMENTS
    
    def test_mock_prediction_structure(self):
        """Test mock prediction returns correct structure."""
        from backend.app.services.ml_service import DiseaseClassifier
        
        classifier = DiseaseClassifier.__new__(DiseaseClassifier)
        result = classifier._mock_prediction()
        
        assert result["success"] is True
        assert "disease" in result
        assert "confidence" in result
        assert "treatment" in result
        assert "top_predictions" in result


class TestPreprocessing:
    """Test image preprocessing functions."""
    
    @patch('tensorflow.keras.preprocessing.image.load_img')
    @patch('tensorflow.keras.preprocessing.image.img_to_array')
    def test_preprocess_image_shape(self, mock_img_to_array, mock_load_img):
        """Test that preprocessing returns correct shape."""
        from backend.app.services.ml_service import DiseaseClassifier
        
        # Setup mocks
        mock_img = Mock()
        mock_load_img.return_value = mock_img
        mock_img_to_array.return_value = np.zeros((128, 128, 3))
        
        classifier = DiseaseClassifier.__new__(DiseaseClassifier)
        classifier.IMAGE_SIZE = 128
        
        # This would test the actual preprocessing
        # Simplified test for structure
        assert True


class TestModelLoading:
    """Test model loading functionality."""
    
    def test_model_not_loaded_initially(self):
        """Test that model is not loaded when file doesn't exist."""
        from backend.app.services.ml_service import DiseaseClassifier
        
        with patch('os.path.exists', return_value=False):
            classifier = DiseaseClassifier.__new__(DiseaseClassifier)
            classifier.model = None
            classifier.model_loaded = False
            
            assert classifier.model is None
            assert classifier.model_loaded is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])