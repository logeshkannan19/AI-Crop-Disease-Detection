# Sample Test Images

This folder contains sample test images for the AI Crop Disease Detection system.

## How to use for testing:

1. **Download PlantVillage Dataset**
   - Visit: https://www.kaggle.com/datasets/abdallahalomari/plantvillage-dataset
   - Extract images to `dataset/train/` and `dataset/test/`

2. **Sample Image Naming Convention**
   - Healthy: `healthy_[number].jpg`
   - Tomato Early Blight: `tomato_early_blight_[number].jpg`
   - Tomato Late Blight: `tomato_late_blight_[number].jpg`
   - Tomato Leaf Mold: `tomato_leaf_mold_[number].jpg`
   - Potato Early Blight: `potato_early_blight_[number].jpg`
   - Potato Late Blight: `potato_late_blight_[number].jpg`

3. **For Demo Purposes**
   - Use any leaf image (128x128 minimum resolution recommended)
   - JPEG, PNG, or WEBP formats supported

## Demo Images Placeholder

Place your test images here:
```
sample_images/
├── healthy_leaf_01.jpg
├── tomato_early_blight_01.jpg
├── tomato_late_blight_01.jpg
└── ...
```

## Expected Output Examples

| Input | Disease | Confidence | Treatment |
|-------|---------|------------|-----------|
| Healthy leaf | Healthy | 95%+ | Continue regular monitoring |
| Blighted leaf | Tomato Early Blight | 88%+ | Apply fungicide, remove infected leaves |
| Moldy leaf | Tomato Leaf Mold | 92%+ | Apply copper fungicide, reduce humidity |