# 🌱 AgriScan AI - AI Crop Disease Detection System

<div align="center">

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-orange.svg)](https://tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-white.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev/)

**An end-to-end AI-powered crop disease detection system for farmers and agricultural businesses.**

*EACE 2026 Exhibition Project | Startup MVP*

</div>

---

## 📋 Table of Contents

1. [Problem Statement](#problem-statement)
2. [Solution Overview](#solution-overview)
3. [Features](#features)
4. [Tech Stack](#tech-stack)
5. [Supported Diseases](#supported-diseases)
6. [Project Structure](#project-structure)
7. [Installation Guide](#installation-guide)
8. [How to Run](#how-to-run)
9. [API Documentation](#api-documentation)
10. [Model Training](#model-training)
11. [Demo Script](#demo-script)
12. [Business Model](#business-model)
13. [Future Roadmap](#future-roadmap)
14. [Team](#team)
15. [License](#license)

---

## 🎯 Problem Statement

### The Challenge

Plant diseases cause significant agricultural losses worldwide:

| Statistic | Impact |
|-----------|--------|
| Global Crop Loss | 20-40% annually |
| Economic Impact | $220+ billion per year |
| Smallholder Farmers | Most vulnerable, limited access to experts |
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

```
┌──────────────┐     ┌─────────────┐     ┌──────────────────┐
│  📸 Upload   │ ──► │     AI      │ ──► │   🎯 Diagnosis   │
│  Leaf Image  │     │  Analysis   │     │   + Treatment    │
└──────────────┘     └─────────────┘     └──────────────────┘
```

### Key Value Propositions

- ⚡ **Fast**: Results in under 2 seconds
- 🎯 **Accurate**: 90%+ accuracy on test data
- 💰 **Affordable**: 10x cheaper than laboratory testing
- 🌐 **Accessible**: Works on any smartphone
- 🌿 **Sustainable**: Promotes targeted pesticide use

---

## ✨ Features

### Core Features
- [x] Image upload (file upload or camera capture)
- [x] Real-time disease classification
- [x] Confidence score display
- [x] Treatment recommendations
- [x] Multiple disease class support
- [x] Clean, farmer-friendly UI
- [x] RESTful API backend
- [x] Model training pipeline
- [x] Health check endpoint
- [x] Interactive API documentation (Swagger UI)

### Supported Diseases (v1.0)

| Class ID | Name | Pathogen | Severity |
|---------|------|---------|-----------|
| 0 | Healthy | - | - |
| 1 | Tomato Early Blight | *Alternaria solani* | Medium |
| 2 | Tomato Late Blight | *Phytophthora infestans* | High |
| 3 | Tomato Leaf Mold | *Passalora fulva* | Low-Medium |
| 4 | Potato Early Blight | *Alternaria solani* | Medium |
| 5 | Potato Late Blight | *Phytophthora infestans* | High |

---

## 🛠 Tech Stack

### Machine Learning
| Technology | Purpose |
|------------|---------|
| TensorFlow 2.15+ | Deep learning framework |
| Keras | High-level neural network API |
| NumPy | Numerical computing |
| CNN | Image classification model |

### Backend
| Technology | Purpose |
|------------|---------|
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Python 3.11+ | Runtime |
| Pillow | Image processing |

### Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI framework |
| Vite | Build tool |
| Axios | HTTP client |
| CSS3 | Styling |

### DevOps
| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Docker Compose | Multi-container setup |
| Git | Version control |
| GitHub Actions | CI/CD |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Frontend)                         │
│   React Web App (Port 5173)                                      │
│   ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │
│   │ Upload     │  │ Results      │  │ API          │           │
│   │ Component  │  │ Display      │  │ Service      │           │
│   └─────────────┘  └──────────────┘  └──────────────┘           │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP (REST API)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND (API)                            │
│   FastAPI Server (Port 8000)                                    │
│   ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │
│   │ API Routes │  │ ML Service   │  │ Config       │           │
│   │ /predict   │  │ Classifier  │  │ Settings    │           │
│   └─────────────┘  └──────────────┘  └──────────────┘           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ML SERVICE (Inference)                       │
│   DiseaseClassifier → Load Model → Preprocess → Predict        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         ML MODEL                                 │
│   Keras CNN Model (plant_disease_model.keras)                     │
│   - Input: 128x128 RGB image                                     │
│   - Architecture: 4 Conv2D blocks + 2 Dense layers           │
│   - Output: 6 class probabilities                              │
└─────────────────────────────────────────────────────────────────┘
```

### Component Details

#### Backend Structure
```
backend/app/
├── __init__.py
├── main.py              # Application entry point
├── api/
│   ├── __init__.py
│   └── prediction.py   # API endpoints
├── core/
│   ├── __init__.py
│   ├── config.py       # Configuration settings
│   └── logging.py     # Logging setup
├── models/
│   └── schemas.py     # Pydantic schemas
└── services/
    ├── __init__.py
    └── ml_service.py  # ML inference service
```

#### ML Structure
```
ml/
├── __init__.py
├── inference/
│   └── inference.py   # Inference module
└── training/
    └── train_model.py # Training script
```

---

## 📂 Project Structure

```
ai-crop-disease-detection/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Configuration
│   │   ├── models/       # Data schemas
│   │   └── services/      # Business logic
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile         # Backend container
│
├── frontend/               # React frontend
│   ├── src/              # React components
│   ├── public/            # Static assets
│   └── package.json      # Node dependencies
│
├── ml/                    # ML module
│   ├── model/            # Trained models
│   ├── training/         # Training scripts
│   └── inference/        # Inference code
│
├── data/                  # Training data
│   ├── train/            # Training images
│   └── test/             # Test images
│
├── docs/                  # Documentation
│   ├── api.md            # API docs
│   ├── architecture.md   # Architecture docs
│   ├── demo.md           # Demo guide
│   ├── demo_script.py    # Demo script
│   └── demo.sh           # Shell demo
│
├── sample_images/         # Demo images
├── tests/                 # Test files
├── docker-compose.yml    # Docker Compose config
├── .env.example          # Environment template
├── LICENSE               # MIT License
└── README.md             # This file
```

---

## ⚙️ Installation Guide

### Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 20 or higher
- **Docker**: 24.0+ (optional but recommended)
- **Git**: For version control
- **Web Browser**: Chrome, Firefox, Safari, or Edge

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/logeshkannan19/AI-Crop-Disease-Detection.git
cd AI-Crop-Disease-Detection

# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn backend.app.main:app --reload

# Backend runs at http://localhost:8000
```

#### Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Frontend runs at http://localhost:5173
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
HOST=0.0.0.0
PORT=8000
MODEL_PATH=ml/model/plant_disease_model.keras
UPLOAD_DIR=backend/app/uploads
LOG_LEVEL=INFO
MAX_FILE_SIZE=10485760
```

---

## ▶️ How to Run

### Quick Start

```bash
# Start backend
cd backend && uvicorn backend.app.main:app --reload

# In another terminal, start frontend
cd frontend && npm run dev
```

### Verify Installation

1. **Health Check**: Visit `http://localhost:8000/api/health`
2. **API Docs**: Visit `http://localhost:8000/docs`
3. **Frontend**: Visit `http://localhost:5173`

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/

# Run specific test
pytest tests/test_api.py -v
```

---

## 📡 API Documentation

### Base URL

```
http://localhost:8000
```

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### 1. Root
```
GET /
```

Returns API information and available endpoints.

**Response:**
```json
{
  "name": "AgriScan AI API",
  "version": "1.0.0",
  "description": "AI-Powered Crop Disease Detection System",
  "docs": "/docs",
  "endpoints": {
    "health": "/api/health",
    "predict": "/api/predict (POST)",
    "classes": "/api/classes (GET)"
  }
}
```

#### 2. Health Check
```
GET /api/health
```

Check if the service is running and model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0"
}
```

#### 3. Predict Disease
```
POST /api/predict
Content-Type: multipart/form-data
```

Predict disease from a plant leaf image.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| file | File | Image file (PNG, JPG, JPEG, GIF, BMP, WEBP) |

**Response:**
```json
{
  "success": true,
  "disease": "Tomato_Early_Blight",
  "disease_readable": "Tomato Early Blight",
  "confidence": 92.5,
  "treatment": "Apply fungicide containing chlorothalonil or copper. Remove infected leaves. Improve air circulation. Avoid overhead watering.",
  "top_predictions": [
    {"disease": "Tomato_Early_Blight", "confidence": 0.925},
    {"disease": "Tomato_Late_Blight", "confidence": 0.052},
    {"disease": "Potato_Early_Blight", "confidence": 0.015}
  ]
}
```

#### 4. Get Classes
```
GET /api/classes
```

Get list of supported disease classes and treatments.

**Response:**
```json
{
  "classes": [
    "Healthy",
    "Tomato_Early_Blight",
    "Tomato_Late_Blight",
    "Tomato_Leaf_Mold",
    "Potato_Early_Blight",
    "Potato_Late_Blight"
  ],
  "treatments": {
    "Healthy": "Plant is healthy! Continue regular watering and monitoring.",
    "Tomato_Early_Blight": "Apply fungicide containing chlorothalonil or copper..."
  }
}
```

### Example Usage

#### Using cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Predict disease
curl -X POST -F "file=@leaf_image.jpg" http://localhost:8000/api/predict

# Get classes
curl http://localhost:8000/api/classes
```

#### Using Python

```python
import requests

# Predict disease
with open("leaf_image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/predict",
        files={"file": f}
    )
    
result = response.json()
print(result["disease"], result["confidence"])
```

---

## 🧠 Model Training

### Training the Model

```bash
cd ml/training
python train_model.py
```

### Training Process

1. **Data Preprocessing**: 
   - Resize images to 128x128
   - Normalize pixel values (0-1)
   - Data augmentation (rotation, flip, zoom)

2. **Model Architecture**:
   - 4 Conv2D + MaxPooling blocks (32, 64, 128, 256 filters)
   - 2 Dense layers (512, 256 neurons)
   - Dropout for regularization (0.5, 0.3)
   - Softmax output (6 classes)

3. **Training Configuration**:
   - Optimizer: Adam (lr=0.001)
   - Loss: Categorical cross-entropy
   - Epochs: 20 (with early stopping)
   - Batch size: 32

4. **Evaluation**:
   - Plots accuracy/loss curves
   - Saves best model checkpoint
   - Exports class mapping JSON

### CNN Architecture

```
Layer 1:  Conv2D(32, 3x3) + MaxPool(2x2)
Layer 2:  Conv2D(64, 3x3) + MaxPool(2x2)
Layer 3:  Conv2D(128, 3x3) + MaxPool(2x2)
Layer 4:  Conv2D(256, 3x3) + MaxPool(2x2)
Flat:     Flatten()
Dense 1:  Dense(512) + Dropout(0.5)
Dense 2:  Dense(256) + Dropout(0.3)
Output:   Dense(6, softmax)
```

### Expected Results

- **Training Accuracy**: ~95%
- **Validation Accuracy**: ~90%
- **Inference Time**: <500ms per image

### Dataset

Download the PlantVillage dataset from Kaggle:
https://www.kaggle.com/datasets/abdallahalomari/plantvillage-dataset

Organize the data as:
```
data/
├── train/
│   ├── Healthy/
│   ├── Tomato_Early_Blight/
│   ├── Tomato_Late_Blight/
│   └── ...
└── test/
    ├── Healthy/
    └── ...
```

---

## 🎤 Demo Script

### For Exhibition Demo (EACE 2026)

Run the demo script:
```bash
cd docs
python demo_script.py
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

## 📊 Future Roadmap

### Phase 2 (Near-term)
- [ ] Add 10+ additional crop types
- [ ] Mobile app (React Native/Flutter)
- [ ] Multi-language support
- [ ] Offline mode with TensorFlow.js

### Phase 3 (Long-term)
- [ ] Drone imagery integration
- [ ] Weather-based disease prediction
- [ ] Community disease tracking map
- [ ] Expert consultation feature

### Technical Improvements
- [ ] Upgrade to ResNet/EfficientNet
- [ ] Transfer learning implementation
- [ ] Object detection (YOLO)
- [ ] Model compression for mobile
- [ ] Edge deployment

---

## 👥 Team

| Role | Name | Contribution |
|------|------|--------------|
| Lead Developer | Logesh Kannan | Full-stack development |
| ML Engineer | AI/ML Team | CNN model training |
| UI/UX Designer | Design Team | User experience |
| Business Lead | Startup Team | Pitch & strategy |

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Dataset**: [PlantVillage](https://www.kaggle.com/datasets/abdallahalomari/plantvillage-dataset) on Kaggle
- **Frameworks**: TensorFlow, FastAPI, React
- **Inspiration**: Farmers and agricultural researchers worldwide

---

<div align="center">

## 🌟 Thank You!

**AgriScan AI** - *Empowering Farmers with AI*

*For demos or inquiries: hello@agriscan.ai*

[![GitHub Stars](https://img.shields.io/github/stars/logeshkannan19/AI-Crop-Disease-Detection?style=social)](https://github.com/logeshkannan19/AI-Crop-Disease-Detection)

[⬆ Back to Top](#table-of-contents)

</div>