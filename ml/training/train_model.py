"""
ML Training Pipeline
====================
Convolutional Neural Network for plant disease classification.
"""

import os
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Flatten, Dense, Dropout
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

# Configuration
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 20
NUM_CLASSES = 6
LEARNING_RATE = 0.001

# Paths
DATA_DIR = Path("data")
MODEL_DIR = Path("ml/model")
TRAIN_PATH = DATA_DIR / "train"
TEST_PATH = DATA_DIR / "test"

# Class names
CLASS_NAMES = [
    "Healthy",
    "Tomato_Early_Blight",
    "Tomato_Late_Blight",
    "Tomato_Leaf_Mold",
    "Potato_Early_Blight",
    "Potato_Late_Blight"
]

# Treatments
TREATMENTS = {
    "Healthy": "Plant is healthy! Continue regular watering and monitoring.",
    "Tomato_Early_Blight": "Apply fungicide containing chlorothalonil or copper. Remove infected leaves. Improve air circulation.",
    "Tomato_Late_Blight": "Apply fungicide immediately. Remove infected plants to prevent spread. Avoid overhead watering.",
    "Tomato_Leaf_Mold": "Apply fungicide containing copper or sulfur. Reduce humidity. Remove infected leaves.",
    "Potato_Early_Blight": "Apply fungicide (mancozeb or chlorothalonil). Remove infected foliage. Crop rotation recommended.",
    "Potato_Late_Blight": "Apply fungicide immediately. Destroy infected plants. Use resistant varieties for next season."
}


def setup_directories():
    """Create necessary directories."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "train").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "test").mkdir(parents=True, exist_ok=True)
    
    for class_name in CLASS_NAMES:
        (DATA_DIR / "train" / class_name).mkdir(exist_ok=True)
        (DATA_DIR / "test" / class_name).mkdir(exist_ok=True)
    
    print(f"Directories created at: {DATA_DIR}")
    print("\nTo train with real data:")
    print("1. Download PlantVillage dataset from Kaggle")
    print("2. Extract to data/train/ and data/test/")
    print("3. Organize as data/train/CLASS_NAME and data/test/CLASS_NAME")


def build_model() -> Sequential:
    """
    Build CNN architecture for plant disease classification.
    
    Architecture:
    - 4 Convolutional blocks with increasing filters
    - MaxPooling after each block
    - Dense layers with dropout for classification
    """
    model = Sequential([
        # Block 1
        Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D((2, 2)),
        
        # Block 2
        Conv2D(64, (3, 3), activation="relu"),
        MaxPooling2D((2, 2)),
        
        # Block 3
        Conv2D(128, (3, 3), activation="relu"),
        MaxPooling2D((2, 2)),
        
        # Block 4
        Conv2D(256, (3, 3), activation="relu"),
        MaxPooling2D((2, 2)),
        
        # Classifier
        Flatten(),
        Dense(512, activation="relu"),
        Dropout(0.5),
        Dense(256, activation="relu"),
        Dropout(0.3),
        Dense(NUM_CLASSES, activation="softmax")
    ])
    
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    print("\n" + "=" * 50)
    print("Model Architecture")
    print("=" * 50)
    model.summary()
    
    return model


def get_data_generators():
    """
    Create image data generators for training and testing.
    
    Applies data augmentation for training data.
    """
    # Training generator with augmentation
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest"
    )
    
    # Test generator (no augmentation)
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)
    
    return train_datagen, test_datagen


def get_generators(train_datagen, test_datagen):
    """Get training and test data generators."""
    train_generator = train_datagen.flow_from_directory(
        TRAIN_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical"
    )
    
    test_generator = test_datagen.flow_from_directory(
        TEST_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical"
    )
    
    return train_generator, test_generator


def train_model():
    """Train the CNN model on the dataset."""
    print("\n" + "=" * 50)
    print("Starting Model Training")
    print("=" * 50)
    
    train_datagen, test_datagen = get_data_generators()
    
    # Check if dataset exists
    if not TRAIN_PATH.exists():
        print(f"\nTraining data not found at {TRAIN_PATH}")
        print("Please add training images and run again.")
        return None
    
    train_generator, test_generator = get_generators(train_datagen, test_datagen)
    
    # Print class indices
    print(f"\nClass indices: {train_generator.class_indices}")
    
    # Build model
    model = build_model()
    
    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            MODEL_DIR / "best_model.keras",
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train
    print("\nTraining started...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=test_generator,
        callbacks=callbacks
    )
    
    # Save final model
    model.save(MODEL_DIR / "plant_disease_model.keras")
    print(f"\nModel saved to: {MODEL_DIR / 'plant_disease_model.keras'}")
    
    # Save training history
    save_training_history(history)
    
    # Save class mapping
    save_class_mapping()
    
    return model, history


def save_training_history(history):
    """Save training history to JSON."""
    history_dict = {
        "accuracy": [float(x) for x in history.history["accuracy"]],
        "val_accuracy": [float(x) for x in history.history["val_accuracy"]],
        "loss": [float(x) for x in history.history["loss"]],
        "val_loss": [float(x) for x in history.history["val_loss"]]
    }
    
    with open(MODEL_DIR / "training_history.json", "w") as f:
        json.dump(history_dict, f, indent=2)
    
    print(f"Training history saved to: {MODEL_DIR / 'training_history.json'}")


def save_class_mapping():
    """Save class names and treatments."""
    mapping = {
        "classes": CLASS_NAMES,
        "treatments": TREATMENTS,
        "class_to_index": {name: idx for idx, name in enumerate(CLASS_NAMES)}
    }
    
    with open(MODEL_DIR / "class_mapping.json", "w") as f:
        json.dump(mapping, f, indent=2)
    
    print(f"Class mapping saved to: {MODEL_DIR / 'class_mapping.json'}")


def evaluate_model():
    """Evaluate trained model on test set."""
    from tensorflow.keras.models import load_model
    
    model_path = MODEL_DIR / "plant_disease_model.keras"
    
    if not model_path.exists():
        print(f"No trained model found at {model_path}")
        return
    
    model = load_model(model_path)
    
    _, test_datagen = get_data_generators()
    test_generator = test_datagen.flow_from_directory(
        TEST_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical"
    )
    
    results = model.evaluate(test_generator)
    
    print("\n" + "=" * 50)
    print("Model Evaluation Results")
    print("=" * 50)
    print(f"Test Loss: {results[0]:.4f}")
    print(f"Test Accuracy: {results[1]:.4f}")


def main():
    """Main training pipeline."""
    # Setup directories
    setup_directories()
    
    # Save class mapping (for API to use)
    save_class_mapping()
    
    # Train model (if data available)
    if TRAIN_PATH.exists() and any(TRAIN_PATH.iterdir()):
        train_model()
    else:
        print("\n" + "=" * 50)
        print("Setup Complete - Awaiting Dataset")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Download PlantVillage dataset from Kaggle")
        print("2. Place images in data/train/ and data/test/")
        print("3. Run: python ml/training/train_model.py")


if __name__ == "__main__":
    main()