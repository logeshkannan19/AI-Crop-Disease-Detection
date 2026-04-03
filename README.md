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

## 📌 Problem Statement

Plant diseases cause devastating losses to global agriculture:

| Metric | Impact |
|--------|--------|
| Global Crop Loss | **20-40%** annually |
| Economic Impact | **$220+ billion** per year |
| Smallholder Farmers | Most vulnerable, limited expert access |
| Early Detection Potential | Can save **80%** of affected crops |

### Why This Matters

- 🍎 **Food Security**: Disease outbreaks threaten global food supply
- 👨‍🌾 **Farmer Livelihoods**: Lost crops = lost income for millions
- 🌍 **Environmental Impact**: Overuse of pesticides due to misdiagnosis
- ⏰ **Time Sensitivity**: Early detection is critical

---

## 💡 Solution Overview

**AgriScan AI** is an intelligent crop disease detection system that empowers farmers with instant, accurate disease diagnosis:

```
┌──────────────┐     ┌─────────────┐     ┌──────────────────┐
│  📸 Upload   │ ──► │     AI      │ ──► │   🎯 Diagnosis   │
│  Leaf Image  │     │  Analysis   │     │   + Treatment    │
└──────────────┘     └─────────────┘     └──────────────────┘
```

### Key Value Propositions

- ⚡ **Fast**: Results in under 2 seconds
- 🎯 **Accurate**: 90%+ accuracy on test data
- 💰 **Affordable**: 10x cheaper than lab testing
- 🌐 **Accessible**: Works on any smartphone
- 🌿 **Sustainable**: Promotes targeted pesticide use

---

## 🧠 AI Model

### Architecture: Convolutional Neural Network (CNN)

```
Input (128x128 RGB) → Conv2D + MaxPool → ... → Dense → Output (6 classes)
```

| Layer | Filters | Details |
|-------|---------|---------|
| Conv2D Block 1 | 32 | 3x3 kernel, ReLU |
| Conv2D Block 2 | 64 | 3x3 kernel, ReLU |
| Conv2D Block 3 | 128 | 3x3 kernel, ReLU |
| Conv2D Block 4 | 256 | 3x3 kernel, ReLU |
| Dense | 512 → 256 | Classification head |

### Supported Diseases (v1.0)

| ID | Class | Description |
|----|-------|-------------|
| 0 | `Healthy` | No disease detected |
| 1 | `Tomato_Early_Blight` | *Alternaria solani* |
| 2 | `Tomato_Late_Blight` | *Phytophthora infestans* |
| 3 | `Tomato_Leaf_Mold` | *Passalora fulva* |
| 4 | `Potato_Early_Blight` | *Alternaria solani* |
| 5 | `Potato_Late_Blight` | *Phytophthora infestans* |

### Training Data

- **Dataset**: PlantVillage (Kaggle)
- **Images**: 15,000+ plant leaf images
- **Preprocessing**: Resize to 128x128, normalize pixels

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          FRONTEND                               │
│  React + Vite (Port 5173/3000)                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Upload      │  │ Results      │  │ API          │          │
│  │ Component   │  │ Display     │  │ Service      │          │
│  └─────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP (REST API)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                          BACKEND                               │
│  FastAPI (Port 8000)                                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ API Routes  │  │ ML Service   │  │ Config       │          │
│  │ /predict    │  │ Classifier   │  │ Settings     │          │
│  └─────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                          ML MODEL                              │
│  TensorFlow/Keras                                              │
│  plant_disease_model.keras                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Vite, CSS3 |
| **Backend** | FastAPI, Uvicorn, Python 3.11+ |
| **ML/AI** | TensorFlow 2.15, Keras, NumPy |
| **DevOps** | Docker, Docker Compose, GitHub Actions |
| **Testing** | pytest, pytest-asyncio, httpx |

---

## 📸 Screenshots / UI

### Web Interface
- Clean, farmer-friendly design
- Drag-and-drop image upload
- Real-time analysis with loading state
- Color-coded results (Green = Healthy, Red = Disease)
- Treatment recommendations displayed prominently

### API Documentation
- Interactive Swagger UI at `/docs`
- ReDoc alternative at `/redoc`

---

## ▶️ How to Run

### Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 20 or higher
- **Docker**: 24.0+ (optional)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-repo/ai-crop-disease-detection.git
cd ai-crop-disease-detection

# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

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

### Training the Model (Optional)

```bash
# Download PlantVillage dataset and place in data/train/ and data/test/
# Then run:
python ml/training/train_model.py
```

---

## 📦 Deployment

### Docker Production Build

```bash
# Build images
docker-compose -f docker-compose.yml build

# Run in production mode
docker-compose -f docker-compose.yml up -d
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
HOST=0.0.0.0
PORT=8000
MODEL_PATH=ml/model/plant_disease_model.keras
UPLOAD_DIR=backend/app/uploads
LOG_LEVEL=INFO
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
- [ ] Edge deployment

---

## 🤝 Contribution Guide

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

Please ensure code quality with proper linting and tests.

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

[![GitHub Stars](https://img.shields.io/github/stars/agriscan-ai/ai-crop-disease-detection?style=social)](https://github.com/agriscan-ai)
[![Follow](https://img.shields.io/twitter/follow/AgriScanAI)](https://twitter.com/AgriScanAI)

</div>