# Data Directory

This directory should contain the training and testing datasets.

## Structure

```
data/
├── train/
│   ├── Healthy/
│   ├── Tomato_Early_Blight/
│   ├── Tomato_Late_Blight/
│   ├── Tomato_Leaf_Mold/
│   ├── Potato_Early_Blight/
│   └── Potato_Late_Blight/
│
└── test/
    ├── Healthy/
    ├── Tomato_Early_Blight/
    ├── Tomato_Late_Blight/
    ├── Tomato_Leaf_Mold/
    ├── Potato_Early_Blight/
    └── Potato_Late_Blight/
```

## Dataset Source

We recommend using the **PlantVillage** dataset:

- **Source**: [Kaggle - PlantVillage Dataset](https://www.kaggle.com/datasets/abdallahalomari/plantvillage-dataset)
- **Images**: 15,000+ images of plant leaves
- **Classes**: 38 crop-disease combinations
- **Format**: 256x256 RGB JPEG images

## Setup Instructions

1. Download the dataset from Kaggle
2. Extract the archive
3. Organize images into the folder structure shown above
4. For this MVP, we use a subset of 6 classes

## Note

Do not commit large dataset files to Git. This directory is tracked but dataset files should be added to `.gitignore`.