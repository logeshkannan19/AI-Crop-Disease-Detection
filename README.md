# AgriScan AI - Crop Disease Detection System

<div align="center">

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-orange.svg)](https://tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-white.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev/)

**AI-Powered Crop Disease Detection for Modern Agriculture**

*EACE 2026 Exhibition Project | Startup MVP*

</div>

---

## Overview

AgriScan AI is an end-to-end machine learning system designed to detect and classify plant diseases from leaf images. Built with TensorFlow/FastAPI/React, it provides farmers and agricultural businesses with instant, accurate disease diagnosis and treatment recommendations.

---

## Problem Statement

Plant diseases cause significant agricultural losses worldwide:

| Metric | Impact |
|--------|-------|
| Global Crop Loss | 20-40% annually |
| Economic Impact | $220+ billion per year |
| Detection Time | Often too late when diseases spread |

Early detection can save up to 80% of affected crops.

---

## Solution

The system processes leaf images through a Convolutional Neural Network (CNN) to identify disease types:

```
Image Upload → AI Analysis → Disease Diagnosis + Treatment
```

Key Value Propositions:
- Results in under 2 seconds
- 90%+ accuracy on test data
- Cost-effective alternative to laboratory testing
- Works on any smartphone

---

## Supported Diseases (v1.0)

| ID | Disease | Pathogen | Severity |
|----|---------|----------|----------|----------|
| 0 | Healthy | - | - |
| 1 | Tomato Early Blight | *Alternaria solani* | Medium |
| 2 | Tomato Late Blight | *Phytophthora infestans* | High |
| 3 | Tomato Leaf Mold | *Passalora fulva* | Low-Medium |
| 4 | Potato Early Blight | *Alternaria solani* | Medium |
| 5 | Potato Late Blight | *Phytophthora infestans* | High |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| ML Framework | TensorFlow 2.15+, Keras |
| Backend | FastAPI, Uvicorn, Python 3.11+ |
| Frontend | React 18, Vite |
| Database | JSON (class mappings) |
| DevOps | Docker, Docker Compose |

---

## Architecture

```
┌────────────────┐     ┌────────────────┐     ┌─────────────────┐
│   Frontend     │ ──► │   FastAPI      │ ──► │   TensorFlow    │
│   (React)      │     │   Backend     │     │   CNN Model     │
└────────────────┘     └────────────────┘     └─────────────────┘
       Port 5173            Port 8000              Inference
```

### Project Structure

```
ai-crop-disease-detection/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Configuration
│   │   ├── models/       # Data schemas
│   │   └── services/      # ML service
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── ml/
│   ├── model/            # Trained models
│   ├── training/         # Training scripts
│   └── inference/        # Inference code
├── data/                  # Training data
├── docs/                  # Documentation
├── tests/                 # Test files
├── docker-compose.yml
└── README.md
```

---

## Quick Start

### Using Docker

```bash
git clone https://github.com/logeshkannan19/AI-Crop-Disease-Detection.git
cd AI-Crop-Disease-Detection
docker-compose up --build
```

### Manual Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-----------|
| GET | `/api/health` | Health check |
| POST | `/api/predict` | Predict disease |
| GET | `/api/classes` | Get supported classes |

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example Request

```bash
curl -X POST -F "file=@leaf_image.jpg" http://localhost:8000/api/predict
```

### Response

```json
{
  "success": true,
  "disease": "Tomato_Early_Blight",
  "confidence": 92.5,
  "treatment": "Apply fungicide containing chlorothalonil..."
}
```

---

## Model Training

```bash
cd ml/training
python train_model.py
```

**Configuration:**
- Image size: 128x128
- Epochs: 20
- Batch size: 32
- Optimizer: Adam (lr=0.001)
- Architecture: 4 Conv2D blocks + 2 Dense layers

**Expected Performance:**
- Training Accuracy: ~95%
- Validation Accuracy: ~90%
- Inference Time: <500ms

---

## Business Model

| Tier | Description | Price |
|------|------------|-------|
| Freemium | Basic scans | Free |
| Premium | Unlimited + history | $4.99/mo |
| Enterprise | API + analytics | Custom |

**Target Market:** 500M+ smallholder farmers, agricultural cooperatives

---

## Future Roadmap

- Add 10+ crop types
- Mobile app (iOS/Android)
- Multi-language support
- Offline mode (TensorFlow.js)
- Drone imagery integration

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Dataset: [PlantVillage](https://www.kaggle.com/datasets/abdallahalomari/plantvillage-dataset)
- Frameworks: TensorFlow, FastAPI, React

---

<div align="center">

*For inquiries: hello@agriscan.ai*

</div>