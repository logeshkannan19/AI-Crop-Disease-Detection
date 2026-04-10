"""
Extended Transfer Learning Training Pipeline
============================================
Supports 7 crops with 27 disease classes using EfficientNetB0.
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
NUM_CLASSES = 27
LEARNING_RATE = 0.0001

DATA_DIR = Path("data")
MODEL_DIR = Path("ml/model")
TRAIN_PATH = DATA_DIR / "train"
TEST_PATH = DATA_DIR / "test"

CLASS_NAMES = [
    "Healthy",
    "Tomato_Early_Blight", "Tomato_Late_Blight", "Tomato_Leaf_Mold",
    "Tomato_Septoria_Leaf_Spot", "Tomato_Spider_Mites", "Tomato_Yellow_Curl_Virus",
    "Potato_Early_Blight", "Potato_Late_Blight", "Potato_Common_Scab", "Potato_Black_Leg",
    "Corn_Common_Rust", "Corn_Northern_Leaf_Blight", "Corn_Gray_Leaf_Spot", "Corn_Southern_Leaf_Blight",
    "Wheat_Leaf_Rust", "Wheat_Powdery_Mildew", "Wheat_Septoria_Blotch",
    "Rice_Blast", "Rice_Bacterial_Leaf_Blight", "Rice_Sheath_Blight",
    "Grape_Black_Rot", "Grape_Esca", "Grape_Leaf_Blight",
    "Apple_Apple_Scab", "Apple_Black_Rot", "Apple_Cedar_Apple_Rust"
]

CROPS = {
    "Tomato": ["Tomato_Early_Blight", "Tomato_Late_Blight", "Tomato_Leaf_Mold",
               "Tomato_Septoria_Leaf_Spot", "Tomato_Spider_Mites", "Tomato_Yellow_Curl_Virus"],
    "Potato": ["Potato_Early_Blight", "Potato_Late_Blight", "Potato_Common_Scab", "Potato_Black_Leg"],
    "Corn": ["Corn_Common_Rust", "Corn_Northern_Leaf_Blight", "Corn_Gray_Leaf_Spot", "Corn_Southern_Leaf_Blight"],
    "Wheat": ["Wheat_Leaf_Rust", "Wheat_Powdery_Mildew", "Wheat_Septoria_Blotch"],
    "Rice": ["Rice_Blast", "Rice_Bacterial_Leaf_Blight", "Rice_Sheath_Blight"],
    "Grape": ["Grape_Black_Rot", "Grape_Esca", "Grape_Leaf_Blight"],
    "Apple": ["Apple_Apple_Scab", "Apple_Black_Rot", "Apple_Cedar_Apple_Rust"]
}

TREATMENTS = {
    "Healthy": "Plant is healthy! Continue regular monitoring.",
    "Tomato_Early_Blight": "Apply chlorothalonil fungicide. Remove infected leaves.",
    "Tomato_Late_Blight": "Apply fungicide immediately. Remove infected plants.",
    "Tomato_Leaf_Mold": "Apply copper fungicide. Reduce humidity.",
    "Tomato_Septoria_Leaf_Spot": "Apply fungicide. Remove infected leaves.",
    "Tomato_Spider_Mites": "Apply miticide. Increase humidity.",
    "Tomato_Yellow_Curl_Virus": "Remove infected plants. Control whitefly vectors.",
    "Potato_Early_Blight": "Apply mancozeb fungicide. Crop rotation.",
    "Potato_Late_Blight": "Apply fungicide immediately. Destroy infected plants.",
    "Potato_Common_Scab": "Maintain low soil pH. Use resistant varieties.",
    "Potato_Black_Leg": "Improve drainage. Remove infected plants.",
    "Corn_Common_Rust": "Apply triazole fungicide. Plant resistant hybrids.",
    "Corn_Northern_Leaf_Blight": "Apply fungicide. Remove crop residue.",
    "Corn_Gray_Leaf_Spot": "Apply strobilurin fungicide. Rotate crops.",
    "Corn_Southern_Leaf_Blight": "Apply fungicide. Plant resistant varieties.",
    "Wheat_Leaf_Rust": "Apply triazole fungicide. Plant resistant varieties.",
    "Wheat_Powdery_Mildew": "Apply sulfur fungicide. Improve air circulation.",
    "Wheat_Septoria_Blotch": "Apply fungicide. Remove crop residue.",
    "Rice_Blast": "Apply tricyclazole. Use resistant varieties.",
    "Rice_Bacterial_Leaf_Blight": "Use resistant varieties. Avoid wounding.",
    "Rice_Sheath_Blight": "Apply fungicide. Reduce plant density.",
    "Grape_Black_Rot": "Apply mancozeb fungicide. Improve air circulation.",
    "Grape_Esca": "No effective treatment. Remove infected vines.",
    "Grape_Leaf_Blight": "Apply copper fungicide. Remove infected leaves.",
    "Apple_Apple_Scab": "Apply captan at bud break. Remove fallen leaves.",
    "Apple_Black_Rot": "Apply fungicide. Remove cankered branches.",
    "Apple_Cedar_Apple_Rust": "Apply fungicide. Remove nearby cedar trees."
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
    print(f"Total classes: {NUM_CLASSES}")
    print("\nSupported crops: " + ", ".join(CROPS.keys()))


def build_model() -> Model:
    """Build EfficientNetB0 transfer learning model."""
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
    
    print(f"\nBase model params: {base_model.count_params():,}")
    return model


def fine_tune(model: Model) -> Model:
    """Fine-tune by unfreezing top layers."""
    base_model = model.layers[0]
    base_model.trainable = True
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE / 10),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


def get_generators():
    """Get training and test data generators."""
    train_gen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.efficientnet.preprocess_input,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )
    
    test_gen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.efficientnet.preprocess_input
    )
    
    return train_gen, test_gen


def train_model():
    """Train the multi-crop model."""
    print("\n" + "=" * 50)
    print("Multi-Crop Disease Detection Training")
    print("=" * 50)
    
    train_gen, test_gen = get_generators()
    
    if not TRAIN_PATH.exists():
        print(f"\nData not found at {TRAIN_PATH}")
        return None
    
    train_generator = train_gen.flow_from_directory(
        TRAIN_PATH, target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE, class_mode="categorical"
    )
    test_generator = test_gen.flow_from_directory(
        TEST_PATH, target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE, class_mode="categorical"
    )
    
    print(f"Classes: {train_generator.class_indices}")
    
    model = build_model()
    
    callbacks = [
        EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
        ModelCheckpoint(MODEL_DIR / "multicrop_best.keras", monitor="val_accuracy", save_best_only=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3)
    ]
    
    print("\nPhase 1: Training classifier head...")
    history = model.fit(train_generator, epochs=EPOCHS, validation_data=test_generator, callbacks=callbacks)
    
    print("\nPhase 2: Fine-tuning...")
    model = fine_tune(model)
    history_fine = model.fit(train_generator, epochs=5, validation_data=test_generator)
    
    model.save(MODEL_DIR / "plant_disease_multicrop.keras")
    
    for k in history_fine.history:
        history.history[k] = history.history.get(k, []) + history_fine.history[k]
    
    save_artifacts(history)
    return model


def save_artifacts(history):
    """Save model artifacts."""
    with open(MODEL_DIR / "multicrop_history.json", "w") as f:
        json.dump({k: [float(v) for v in vs] for k, vs in history.history.items()}, f, indent=2)
    
    mapping = {
        "classes": CLASS_NAMES,
        "crops": CROPS,
        "treatments": TREATMENTS,
        "model_type": "EfficientNetB0_MultiCrop",
        "input_size": IMG_SIZE,
        "num_classes": NUM_CLASSES
    }
    with open(MODEL_DIR / "multicrop_classes.json", "w") as f:
        json.dump(mapping, f, indent=2)
    
    print(f"\nArtifacts saved to {MODEL_DIR}")


def main():
    setup_directories()
    save_artifacts(type('obj', (object,), {'history': {}})())
    
    if TRAIN_PATH.exists() and any(TRAIN_PATH.iterdir()):
        train_model()
    else:
        print("\nAwaiting dataset. Download PlantVillage dataset and organize in data/train/")


if __name__ == "__main__":
    main()
