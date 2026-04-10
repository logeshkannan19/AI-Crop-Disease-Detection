"""
Transfer Learning Training Pipeline
====================================
Uses EfficientNetB0 pre-trained on ImageNet for plant disease classification.
This approach typically achieves 95%+ accuracy with fewer epochs.
"""

import os
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    Dense, Dropout, GlobalAveragePooling2D, Input
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import EfficientNetB0

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 15
NUM_CLASSES = 6
LEARNING_RATE = 0.0001

DATA_DIR = Path("data")
MODEL_DIR = Path("ml/model")
TRAIN_PATH = DATA_DIR / "train"
TEST_PATH = DATA_DIR / "test"

CLASS_NAMES = [
    "Healthy",
    "Tomato_Early_Blight",
    "Tomato_Late_Blight",
    "Tomato_Leaf_Mold",
    "Potato_Early_Blight",
    "Potato_Late_Blight"
]

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


def build_transfer_model() -> Model:
    """
    Build transfer learning model using EfficientNetB0.
    
    Architecture:
    - EfficientNetB0 base (ImageNet pre-trained, frozen)
    - GlobalAveragePooling2D
    - Dense(512) + Dropout(0.5)
    - Dense(256) + Dropout(0.3)
    - Dense(NUM_CLASSES, softmax)
    """
    base_model = EfficientNetB0(
        weights="imagenet",
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    
    base_model.trainable = False
    
    model = Sequential([
        Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        base_model,
        GlobalAveragePooling2D(),
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
    print("Transfer Learning Model (EfficientNetB0)")
    print("=" * 50)
    print(f"Base model parameters: {base_model.count_params():,}")
    model.summary()
    
    return model


def unfreeze_top_layers(model: Model, unfreeze_epochs: int = 5) -> Model:
    """
    Fine-tune by unfreezing top layers of EfficientNet.
    This typically improves accuracy further.
    """
    print("\n" + "=" * 50)
    print("Fine-tuning: Unfreezing top layers")
    print("=" * 50)
    
    base_model = model.layers[0]
    base_model.trainable = True
    
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    for layer in base_model.layers[-20:]:
        layer.trainable = True
    
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE / 10),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    print(f"Unfrozen {sum(1 for l in base_model.layers if l.trainable)} layers")
    
    return model


def get_data_generators():
    """
    Create image data generators with preprocessing for EfficientNet.
    """
    train_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.efficientnet.preprocess_input,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest"
    )
    
    test_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.efficientnet.preprocess_input
    )
    
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
    """Train the transfer learning model."""
    print("\n" + "=" * 50)
    print("Starting Transfer Learning Training")
    print("=" * 50)
    
    train_datagen, test_datagen = get_data_generators()
    
    if not TRAIN_PATH.exists():
        print(f"\nTraining data not found at {TRAIN_PATH}")
        print("Please add training images and run again.")
        return None
    
    train_generator, test_generator = get_generators(train_datagen, test_datagen)
    
    print(f"\nClass indices: {train_generator.class_indices}")
    print(f"Training samples: {train_generator.samples}")
    print(f"Test samples: {test_generator.samples}")
    
    model = build_transfer_model()
    
    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            MODEL_DIR / "efficientnet_trained.keras",
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            verbose=1
        )
    ]
    
    print("\nPhase 1: Training classifier head...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=test_generator,
        callbacks=callbacks
    )
    
    print("\n" + "=" * 50)
    print("Phase 2: Fine-tuning (unfreezing top layers)...")
    print("=" * 50)
    
    model = unfreeze_top_layers(model)
    
    fine_tune_callbacks = [
        ModelCheckpoint(
            MODEL_DIR / "efficientnet_finetuned.keras",
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            verbose=1
        )
    ]
    
    history_fine = model.fit(
        train_generator,
        epochs=5,
        validation_data=test_generator,
        callbacks=fine_tune_callbacks
    )
    
    model.save(MODEL_DIR / "plant_disease_efficientnet.keras")
    print(f"\nFinal model saved to: {MODEL_DIR / 'plant_disease_efficientnet.keras'}")
    
    for h in history_fine.history:
        history.history[h] = history.history.get(h, []) + history_fine.history[h]
    
    save_training_history(history)
    save_class_mapping()
    
    return model, history


def save_training_history(history):
    """Save training history to JSON."""
    history_dict = {
        "accuracy": [float(x) for x in history.history.get("accuracy", [])],
        "val_accuracy": [float(x) for x in history.history.get("val_accuracy", [])],
        "loss": [float(x) for x in history.history.get("loss", [])],
        "val_loss": [float(x) for x in history.history.get("val_loss", [])]
    }
    
    with open(MODEL_DIR / "training_history.json", "w") as f:
        json.dump(history_dict, f, indent=2)
    
    print(f"Training history saved to: {MODEL_DIR / 'training_history.json'}")


def save_class_mapping():
    """Save class names and treatments."""
    mapping = {
        "classes": CLASS_NAMES,
        "treatments": TREATMENTS,
        "class_to_index": {name: idx for idx, name in enumerate(CLASS_NAMES)},
        "model_type": "EfficientNetB0",
        "input_size": IMG_SIZE
    }
    
    with open(MODEL_DIR / "class_mapping.json", "w") as f:
        json.dump(mapping, f, indent=2)
    
    print(f"Class mapping saved to: {MODEL_DIR / 'class_mapping.json'}")


def evaluate_model():
    """Evaluate trained model on test set."""
    from tensorflow.keras.models import load_model
    
    model_path = MODEL_DIR / "plant_disease_efficientnet.keras"
    
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
    setup_directories()
    save_class_mapping()
    
    if TRAIN_PATH.exists() and any(TRAIN_PATH.iterdir()):
        train_model()
    else:
        print("\n" + "=" * 50)
        print("Setup Complete - Awaiting Dataset")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Download PlantVillage dataset from Kaggle")
        print("2. Place images in data/train/ and data/test/")
        print("3. Run: python ml/training/train_transfer_model.py")


if __name__ == "__main__":
    main()
