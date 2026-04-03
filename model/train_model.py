#!/usr/bin/env python3
"""
AI Crop Disease Detection - CNN Model Training
================================================
This script trains a Convolutional Neural Network for plant disease classification.
Dataset: PlantVillage (simulated structure for student project)

Classes:
- Healthy
- Tomato Early Blight
- Tomato Late Blight
- Tomato Leaf Mold
- Potato Early Blight
- Potato Late Blight

Author: AgriTech AI Team
Project: EACE 2026 Exhibition
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt

# Configuration
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 20
NUM_CLASSES = 6
DATASET_PATH = 'dataset'

CLASS_NAMES = [
    'Healthy',
    'Tomato_Early_Blight',
    'Tomato_Late_Blight',
    'Tomato_Leaf_Mold',
    'Potato_Early_Blight',
    'Potato_Late_Blight'
]

TREATMENTS = {
    'Healthy': 'Plant is healthy! Continue regular watering and monitoring.',
    'Tomato_Early_Blight': 'Apply fungicide containing chlorothalonil or copper. Remove infected leaves. Improve air circulation.',
    'Tomato_Late_Blight': 'Apply fungicide immediately. Remove infected plants to prevent spread. Avoid overhead watering.',
    'Tomato_Leaf_Mold': 'Apply fungicide containing copper or sulfur. Reduce humidity. Remove infected leaves.',
    'Potato_Early_Blight': 'Apply fungicide (mancozeb or chlorothalonil). Remove infected foliage. Crop rotation recommended.',
    'Potato_Late_Blight': 'Apply fungicide immediately. Destroy infected plants. Use resistant varieties for next season.'
}


def create_synthetic_dataset():
    """Create synthetic dataset structure for demonstration."""
    print("Creating synthetic dataset structure...")
    
    for class_name in CLASS_NAMES:
        class_path = os.path.join(DATASET_PATH, 'train', class_name)
        os.makedirs(class_path, exist_ok=True)
        
        test_path = os.path.join(DATASET_PATH, 'test', class_name)
        os.makedirs(test_path, exist_ok=True)
    
    print(f"Dataset structure created at: {DATASET_PATH}")
    print("\nTo train with real data:")
    print("1. Download PlantVillage dataset from Kaggle")
    print("2. Extract to the dataset/ folder")
    print("3. Organize as dataset/train/CLASS_NAME and dataset/test/CLASS_NAME")


def build_model():
    """Build CNN architecture for image classification."""
    model = Sequential([
        # First Convolutional Block
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D((2, 2)),
        
        # Second Convolutional Block
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # Third Convolutional Block
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # Fourth Convolutional Block
        Conv2D(256, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # Flatten and Dense Layers
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.3),
        Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.summary()
    return model


def train_model():
    """Train the CNN model on the dataset."""
    # Data augmentation and preprocessing
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Check if dataset exists
    train_path = os.path.join(DATASET_PATH, 'train')
    test_path = os.path.join(DATASET_PATH, 'test')
    
    if not os.path.exists(train_path):
        create_synthetic_dataset()
        print("\nPlease add training images to dataset/train/CLASS_NAME/")
        print("Exiting. Run again after adding data.")
        return None
    
    # Load training data
    try:
        train_generator = train_datagen.flow_from_directory(
            train_path,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical'
        )
        
        test_generator = test_datagen.flow_from_directory(
            test_path,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical'
        )
    except Exception as e:
        print(f"Error loading data: {e}")
        print("\nPlease ensure dataset structure is correct.")
        return None
    
    # Build and train model
    model = build_model()
    
    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ModelCheckpoint('model/best_model.keras', monitor='val_accuracy', save_best_only=True)
    ]
    
    # Train
    print("\nStarting training...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=test_generator,
        callbacks=callbacks
    )
    
    # Save final model
    model.save('model/plant_disease_model.keras')
    print("\nModel saved to model/plant_disease_model.keras")
    
    # Plot training history
    plot_training_history(history)
    
    return model, history


def plot_training_history(history):
    """Plot accuracy and loss graphs."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Accuracy plot
    axes[0].plot(history.history['accuracy'], label='Training Accuracy', marker='o')
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', marker='s')
    axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Loss plot
    axes[1].plot(history.history['loss'], label='Training Loss', marker='o')
    axes[1].plot(history.history['val_loss'], label='Validation Loss', marker='s')
    axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('model/training_history.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Training graphs saved to model/training_history.png")


def evaluate_model():
    """Evaluate trained model on test set."""
    from tensorflow.keras.models import load_model
    
    if not os.path.exists('model/plant_disease_model.keras'):
        print("No trained model found. Please train the model first.")
        return
    
    model = load_model('model/plant_disease_model.keras')
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        os.path.join(DATASET_PATH, 'test'),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    results = model.evaluate(test_generator)
    print(f"\nTest Loss: {results[0]:.4f}")
    print(f"Test Accuracy: {results[1]:.4f}")


def save_class_mapping():
    """Save class names and treatments for backend."""
    import json
    
    mapping = {
        'classes': CLASS_NAMES,
        'treatments': TREATMENTS,
        'class_to_index': {name: idx for idx, name in enumerate(CLASS_NAMES)}
    }
    
    with open('model/class_mapping.json', 'w') as f:
        json.dump(mapping, f, indent=2)
    
    print("Class mapping saved to model/class_mapping.json")


if __name__ == '__main__':
    os.makedirs('model', exist_ok=True)
    
    # Create synthetic dataset structure
    create_synthetic_dataset()
    
    # Save class mapping
    save_class_mapping()
    
    print("\n" + "="*60)
    print("SETUP COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Download PlantVillage dataset from Kaggle")
    print("2. Place images in dataset/train/ and dataset/test/")
    print("3. Run: python train_model.py")
    print("\nOr use the pre-trained model for inference.")