# ML Model Directory

This directory contains the trained model files.

## Files

- `plant_disease_model.keras` - Trained CNN model (add after training)
- `class_mapping.json` - Class names and treatments mapping
- `training_history.json` - Training metrics (generated after training)

## How to Get the Model

### Option 1: Train Yourself

Follow the instructions in `ml/training/train_model.py` to train the model using the PlantVillage dataset.

### Option 2: Download Pre-trained

1. Download the PlantVillage dataset from Kaggle
2. Train using the provided script
3. The model will be saved here automatically

### Model Format

The model is saved in Keras format (`.keras`) and can be loaded with:

```python
from tensorflow.keras.models import load_model
model = load_model('ml/model/plant_disease_model.keras')
```

## Model Architecture

```
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 conv2d (Conv2D)             (None, 126, 126, 32)      896       
 max_pooling2d (MaxPooling2D (None, 63, 63, 32)       0         
 conv2d_1 (Conv2D)           (None, 61, 61, 64)        18496     
 max_pooling2d_1 (MaxPooling2 (None, 30, 30, 64)      0         
 conv2d_2 (Conv2D)           (None, 28, 28, 128)       73856     
 max_pooling2d_2 (MaxPooling2 (None, 14, 14, 128)     0         
 conv2d_3 (Conv2D)           (None, 12, 12, 256)       295168    
 max_pooling2d_3 (MaxPooling2 (None, 6, 6, 256)      0         
 flatten (Flatten)           (None, 9216)              0         
 dense (Dense)               (None, 512)               4719104   
 dropout (Dropout)           (None, 512)               0         
 dense_1 (Dense)             (None, 256)               131328    
 dropout_1 (Dropout)         (None, 256)               0         
 dense_2 (Dense)             (None, 6)                 1542      
=================================================================
Total params: 5,243,390
Trainable params: 5,243,390
Non-trainable params: 0
_________________________________________________________________
```