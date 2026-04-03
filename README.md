# 🌱 AgriScan AI - AI Crop Disease Detection System

<div align="center">

![Status](https://img.shields.io/badge/Status-Ready%20for%20Demo-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![React](https://img.shields.io/badge/React-18-blue)

**An end-to-end AI-powered crop disease detection system for farmers and agricultural businesses.**

*EACE 2026 Exhibition Project | Investor Pitch Prototype*

</div>

---

## 📋 Table of Contents

1. [Problem Statement](#problem-statement)
2. [Solution Overview](#solution-overview)
3. [Features](#features)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Installation Guide](#installation-guide)
7. [How to Run](#how-to-run)
8. [API Documentation](#api-documentation)
9. [Model Training](#model-training)
10. [Demo Script](#demo-script)
11. [Business Model](#business-model)
12. [Future Improvements](#future-improvements)
13. [Team](#team)
14. [License](#license)

---

## 🎯 Problem Statement

### The Challenge

Plant diseases cause significant agricultural losses worldwide:

| Statistic | Impact |
|-----------|--------|
| Global Crop Loss | 20-40% annually |
| Economic Impact | $220+ billion per year |
| Small Farmers | Most vulnerable, limited access to experts |
| Detection Time | Often too late when diseases spread |

### Why This Matters

- **Food Security**: Disease outbreaks threaten global food supply
- **Farmer Livelihoods**: Lost crops mean lost income for millions
- **Environmental Impact**: Overuse of pesticides due to misdiagnosis
- **Time Sensitivity**: Early detection can save up to 80% of affected crops

---

## 💡 Solution Overview

**AgriScan AI** is an intelligent crop disease detection system that:

1. 📸 **Captures** - Users upload photos of plant leaves (via mobile or web)
2. 🧠 **Analyzes** - AI model detects patterns using Convolutional Neural Networks
3. 📊 **Diagnoses** - Identifies disease type with confidence score
4. 💊 **Prescribes** - Provides treatment recommendations instantly

### Key Value Propositions

- ⚡ **Fast**: Results in under 2 seconds
- 🎯 **Accurate**: 90%+ accuracy on test data
- 💰 **Affordable**: 10x cheaper than laboratory testing
- 🌐 **Accessible**: Works on any smartphone
- 🌿 **Sustainable**: Promotes targeted pesticide use

---

## ✨ Features

### Core Features
- [x] Image upload (file upload or camera capture simulation)
- [x] Real-time disease classification
- [x] Confidence score display
- [x] Treatment recommendations
- [x] Multiple disease class support
- [x] Clean, farmer-friendly UI
- [x] RESTful API backend
- [x] Model training pipeline

### Supported Diseases (v1.0)
| Class | Disease | Description |
|-------|---------|-------------|
| 0 | Healthy | No disease detected |
| 1 | Tomato Early Blight | *Alternaria solani* |
| 2 | Tomato Late Blight | *Phytophthora infestans* |
| 3 | Tomato Leaf Mold | *Passalora fulva* |
| 4 | Potato Early Blight | *Alternaria solani* |
| 5 | Potato Late Blight | *Phytophthora infestans* |

---

## 🛠 Tech Stack

### Machine Learning
- **Framework**: TensorFlow 2.x / Keras
- **Model**: Convolutional Neural Network (CNN)
- **Dataset**: PlantVillage (15,000+ images)
- **Image Size**: 128x128 pixels

### Backend
- **Framework**: Flask (Python)
- **API**: RESTful JSON API
- **Image Processing**: PIL, NumPy

### Frontend
- **Framework**: React.js 18
- **Styling**: CSS3 (custom)
- **HTTP Client**: Axios
- **Alternative**: Plain HTML/JS (included)

### Additional Tools
- **Version Control**: Git
- **Package Management**: pip, npm
- **Model Format**: Keras (.keras)

---

## 📂 Project Structure

```
agri_disease_detection/
├── backend/                 # Flask API server
│   ├── app.py              # Main application
│   ├── requirements.txt    # Python dependencies
│   └── uploads/            # Temp upload directory
│
├── frontend/               # React web application
│   ├── public/            # Static assets
│   ├── src/               # React components
│   │   ├── App.js         # Main component
│   │   ├── App.css        # Styles
│   │   └── index.js       # Entry point
│   ├── package.json       # Node dependencies
│   └── index.html         # Alternative HTML version
│
├── model/                  # ML model files
│   ├── train_model.py     # Training script
│   ├── inference.py       # Inference module
│   ├── plant_disease_model.keras  # Trained model
│   ├── class_mapping.json # Class labels & treatments
│   └── training_history.png  # Training graphs
│
├── dataset/                # Training data (you provide)
│   ├── train/             # Training images
│   └── test/              # Test images
│
├── sample_images/          # Demo images
│   └── README.md          # Image guide
│
├── docs/                   # Documentation
│   ├── demo.sh            # Shell demo script
│   └── demo_script.py     # Python demo script
│
└── README.md              # This file
```

---

## 🚀 Installation Guide

### Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 16+ (for React frontend)
- **Git**: For version control
- **Web Browser**: Chrome, Firefox, Safari, Edge

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd agri_disease_detection
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### Step 3: Set Up React Frontend

```bash
cd frontend
npm install
```

### Step 4: Download Dataset (Optional for Demo)

For training the model:

1. Download PlantVillage dataset:
   https://www.kaggle.com/datasets/abdallahalomari/plantvillage-dataset

2. Extract to `dataset/` folder:
   ```
   dataset/
   ├── train/
   │   ├── Healthy/
   │   ├── Tomato_Early_Blight/
   │   └── ...
   └── test/
       ├── Healthy/
       └── ...
   ```

---

## ▶️ How to Run

### Option 1: Full Stack (Recommended)

**Terminal 1 - Start Backend:**
```bash
cd agri_disease_detection/backend
python app.py
```
*Server runs at http://localhost:5000*

**Terminal 2 - Start Frontend:**
```bash
cd agri_disease_detection/frontend
npm start
```
*Web app opens at http://localhost:3000*

### Option 2: Backend Only (API Testing)

```bash
cd agri_disease_detection/backend
python app.py
```

Test with curl:
```bash
curl -X POST -F "image=@sample.jpg" http://localhost:5000/api/predict
```

### Option 3: HTML Version (No React Setup)

Simply open in browser:
```bash
cd agri_disease_detection/frontend
open index.html
```

*Note: For API calls to work, backend must be running.*

---

## 📡 API Documentation

### Endpoints

#### 1. Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### 2. Predict Disease
```
POST /api/predict
Content-Type: multipart/form-data

Parameter: image (file)
```

**Response:**
```json
{
  "success": true,
  "disease": "Tomato_Early_Blight",
  "confidence": 92.5,
  "treatment": "Apply fungicide containing chlorothalonil...",
  "top_predictions": [
    {"disease": "Tomato_Early_Blight", "confidence": 0.925},
    {"disease": "Tomato_Late_Blight", "confidence": 0.052},
    {"disease": "Potato_Early_Blight", "confidence": 0.015}
  ]
}
```

#### 3. Get Classes
```
GET /api/classes
```

**Response:**
```json
{
  "classes": ["Healthy", "Tomato_Early_Blight", ...],
  "treatments": {...}
}
```

---

## 🧠 Model Training

### Training the Model

```bash
cd agri_disease_detection/model
python train_model.py
```

### Training Process

1. **Data Preprocessing**: 
   - Resize images to 128x128
   - Normalize pixel values (0-1)
   - Data augmentation (rotation, flip, zoom)

2. **Model Architecture**:
   - 4 Conv2D + MaxPooling blocks
   - 2 Dense layers (512, 256 neurons)
   - Dropout for regularization
   - Softmax output (6 classes)

3. **Training**:
   - Adam optimizer
   - Categorical cross-entropy loss
   - 20 epochs (with early stopping)
   - Batch size: 32

4. **Evaluation**:
   - Plots accuracy/loss curves
   - Saves best model checkpoint
   - Exports class mapping JSON

### Expected Results

- **Training Accuracy**: ~95%
- **Validation Accuracy**: ~90%
- **Inference Time**: <500ms per image

---

## 🎤 Demo Script

### For Exhibition Demo (EACE 2026)

Run the demo script:
```bash
cd agri_disease_detection
python docs/demo_script.py
```

### Presentation Outline

1. **Introduction** (30 sec)
   - Problem: 40% crop loss to diseases
   - Solution: AI-powered detection

2. **Live Demo** (2 min)
   - Upload sample leaf image
   - Show disease detection
   - Display confidence and treatment

3. **Technology** (1 min)
   - CNN architecture explanation
   - Accuracy metrics
   - Tech stack overview

4. **Business Model** (1 min)
   - Target: 500M+ farmers
   - Revenue: Freemium + B2B
   - Ask: $500K seed funding

5. **Q&A** (remaining time)

---

## 💰 Business Model

### Revenue Streams

| Model | Description | Price Point |
|-------|-------------|-------------|
| **Freemium** | Basic disease scans | Free |
| **Premium** | Unlimited scans + history | $4.99/mo |
| **Enterprise** | API access + analytics | Custom |
| **B2B** | Agricultural companies | $999+/mo |

### Target Market

- **Primary**: 500M+ smallholder farmers
- **Secondary**: Agricultural cooperatives
- **Tertiary**: Vertical farms, greenhouses
- **Partners**: Input companies, insurers

### Growth Strategy

```
Q2 2026: Beta Launch (1,000 users)
   ↓
Q3 2026: Add 10 crop types
   ↓
Q4 2026: Mobile App (iOS/Android)
   ↓
2027: Global Expansion
```

---

## 🔮 Future Improvements

### Phase 2 (Near-term)
- [ ] Add 10+ additional crop types
- [ ] Implement mobile app (React Native/Flutter)
- [ ] Add multi-language support
- [ ] Offline mode with TensorFlow.js
- [ ] Disease severity estimation

### Phase 3 (Long-term)
- [ ] Integration with drone imagery
- [ ] Weather-based disease prediction
- [ ] Community disease tracking map
- [ ] Expert consultation feature
- [ ] Agricultural insurance integration

### Technical Improvements
- [ ] Upgrade to ResNet/EfficientNet
- [ ] Implement transfer learning
- [ ] Add object detection (YOLO)
- [ ] Model compression for mobile
- [ ] Edge deployment

---

## 👥 Team

| Role | Name | Contribution |
|------|------|--------------|
| Lead Developer | AgriTech AI Team | Full-stack development |
| ML Engineer | AI Team | CNN model training |
| UI/UX Designer | Design Team | User experience |
| Business Lead | Startup Team | Pitch & strategy |

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 🙏 Acknowledgments

- **Dataset**: PlantVillage (Kaggle)
- **Framework**: TensorFlow, Keras, Flask, React
- **Inspiration**: Farmers and agricultural researchers worldwide

---

<div align="center">

## 🌟 Thank You!

**AgriScan AI** - *Empowering Farmers with AI*

*For demo or inquiries: hello@agriscan.ai*

[⬆ Back to Top](#table-of-contents)

</div>