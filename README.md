# AgriScan AI - Crop Disease Detection System

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&weight=700&size=36&color=2E7D32&center=true&vCenter=true&width=800&height=50&lines=AgriScan+AI;Crop+Disease+Detection+System" alt="AgriScan AI" />
</p>

<div align="center">

<p align="center">
  <img src="https://img.shields.io/badge/architecture-Microservices-blue?style=for-the-badge" alt="Architecture" />
  <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/tensorflow-2.15+-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TensorFlow" />
  <img src="https://img.shields.io/badge/fastapi-0.109+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/react-18-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React" />
  <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/status-Production_Ready-success?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License" />
</p>

<p><b>AI-Powered Crop Disease Detection for Modern Agriculture</b></p>

<p>
  <a href="https://github.com/logeshkannan19/AI-Crop-Disease-Detection">
    <img src="https://img.shields.io/github/stars/logeshkannan19/AI-Crop-Disease-Detection?style=social" alt="Stars" />
  </a>
  <a href="https://github.com/logeshkannan19/AI-Crop-Disease-Detection/fork">
    <img src="https://img.shields.io/github/forks/logeshkannan19/AI-Crop-Disease-Detection?style=social" alt="Forks" />
  </a>
  <a href="https://github.com/logeshkannan19/AI-Crop-Disease-Detection/issues">
    <img src="https://img.shields.io/github/issues/logeshkannan19/AI-Crop-Disease-Detection" alt="Issues" />
  </a>
  <a href="https://github.com/logeshkannan19/AI-Crop-Disease-Detection/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/logeshkannan19/AI-Crop-Disease-Detection/ci-cd.yml" alt="CI/CD" />
  </a>
</p>

<p>
  <img src="https://api.visitorbadge.io/api/visitors?path=logeshkannan19%2FAI-Crop-Disease-Detection&label=visitors&countColor=%232E7D32" alt="Visitors" />
  <img src="https://img.shields.io/github/last-commit/logeshkannan19/AI-Crop-Disease-Detection/main" alt="Last Commit" />
  <img src="https://img.shields.io/github/contributors/logeshkannan19/AI-Crop-Disease-Detection" alt="Contributors" />
</p>

<p><i>🏆 EACE 2026 Exhibition Project | 🚀 Startup MVP</i></p>

</div>

---

## 📋 Table of Contents

- [About](#about)
- [Problem Statement](#problem-statement)
- [How It Works](#how-it-works)
- [System Architecture](#system-architecture)
- [Model Architecture](#model-architecture)
- [Supported Diseases](#supported-diseases)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Model Training](#model-training)
- [Testing](#testing)
- [Business Model](#business-model)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

## 📖 About

**AgriScan AI** is an end-to-end machine learning system designed to detect and classify plant diseases from leaf images. Built with **TensorFlow**, **FastAPI**, and **React**, it provides farmers and agricultural businesses with instant, accurate disease diagnosis and treatment recommendations.

The system leverages deep learning (Convolutional Neural Networks) to analyze plant leaf imagery, identify disease patterns, and provide actionable treatment guidance—all within seconds.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| ⚡ **Real-time Detection** | Results in under 2 seconds |
| 🎯 **High Accuracy** | 90%+ accuracy on test data |
| 💊 **Treatment Recommendations** | Provides actionable disease management advice |
| 🌐 **RESTful API** | Easy integration with existing systems |
| 🐳 **Containerized** | Docker Compose for easy deployment |
| 📱 **Mobile Friendly** | Works on any smartphone |

---

## 🎯 Features

### Core Features

| | |
|---|---|
| <h3>🔍 Intelligent Disease Detection</h3> | Advanced CNN model trained on 20,000+ plant images to identify diseases with 90%+ accuracy |
| <h3>💊 Treatment Recommendations</h3> | AI-generated treatment plans including fungicide suggestions, prevention tips, and management strategies |
| <h3>⚡ Real-time Processing</h3> | Sub-second inference time using optimized TensorFlow model with batch processing support |
| <h3>🖼️ Multi-format Image Support</h3> | Accepts JPEG, PNG, and WebP images up to 10MB with automatic preprocessing |
| <h3>📊 Confidence Scoring</h3> | Detailed probability scores for each prediction to help prioritize actions |
| <h3>🌐 RESTful API</h3> | Well-documented API with Swagger UI for easy integration and testing |

### Advanced Features

| | |
|---|---|
| <h3>🔒 Secure File Handling</h3> | Input validation, file type restrictions, size limits, and path traversal prevention |
| <h3>📈 Batch Processing</h3> | Process multiple images simultaneously for large-scale disease screening |
| <h3>📱 Responsive Design</h3> | Mobile-first UI that works seamlessly across devices and screen sizes |
| <h3>🌊 API Rate Limiting</h3> | Configurable rate limits to prevent abuse and ensure fair usage |
| <h3>📝 Detailed Logging</h3> | Comprehensive logging for debugging, monitoring, and analytics |
| <h3>🔄 Auto-scaling</h3> | Docker Compose configuration for horizontal scaling in production |

### ML/AI Features

| | |
|---|---|
| <h3>🧠 Custom CNN Architecture</h3> | 4-block convolutional network with batch normalization and dropout |
| <h3>📊 Transfer Learning Ready</h3> | Architecture designed for easy fine-tuning with pre-trained weights |
| <h3>🔧 Model Versioning</h3> | Support for multiple model versions with seamless switching |
| <h3>📉 Training Analytics</h3> | Built-in support for training metrics, confusion matrices, and loss curves |
| <h3>🎚️ Data Augmentation</h3> | Real-time augmentation including rotation, flip, zoom, and brightness adjustment |
| <h3>💾 Model Export</h3> | Export trained models in standard formats (.h5, .keras, SavedModel) |

### Developer Features

| | |
|---|---|
| <h3>📚 Interactive Documentation</h3> | Auto-generated Swagger UI and ReDoc for comprehensive API documentation |
| <h3>🐛 Debug Mode</h3> | Detailed error messages and stack traces in development environment |
| <h3>🧪 Test Coverage</h3> | Unit tests for API endpoints, model loading, and preprocessing |
| <h3>🔄 CI/CD Pipeline</h3> | GitHub Actions workflow for automated testing and deployment |
| <h3>📦 Docker Support</h3> | Production-ready Docker images with multi-stage builds |
| <h3>⚙️ Environment Config</h3> | Environment-based configuration for different deployment scenarios |

### Operational Features

| | |
|---|---|
| <h3>📊 Health Monitoring</h3> | Health check endpoints for container orchestration and load balancers |
| <h3>📈 Performance Metrics</h3> | API metrics including response times, prediction counts, and error rates |
| <h3>🔄 Hot Reload</h3> | Development mode with automatic code reloading |
| <h3>🌐 CORS Enabled</h3> | Cross-origin resource sharing configured for frontend integration |
| <h3>📁 File Management</h3> | Automatic cleanup of uploaded files to prevent storage bloat |
| <h3>🛡️ Error Handling</h3> | Graceful error handling with user-friendly messages |

### 🎯 Target Audience

- 🌾 Smallholder farmers
- 🚜 Agricultural cooperatives
- 🏢 Farm management companies
- 🔬 Agricultural research institutions
- 🌿 Agricultural input suppliers

---

## ⚠️ Problem Statement

Plant diseases cause significant agricultural losses worldwide, threatening food security and farmer livelihoods.

### 📊 Global Impact

| Metric | Impact | Source |
|--------|--------|--------|
| Global Crop Loss | **20-40%** annually | [FAO](https://www.fao.org/) |
| Economic Impact | **$220+ billion** per year | [World Bank](https://www.worldbank.org/) |
| Detection Time | Often too late when diseases spread | Research |
| Smallholder Impact | Most vulnerable to losses | [IFAD](https://www.ifad.org/) |

### 🔥 Why Early Detection Matters

```
┌────────────────────────────────────────────────────────────────────┐
│                     EARLY DETECTION BENEFITS                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   ✓ Save up to 80% of affected crops                              │
│   ✓ Prevent disease spread to healthy plants                      │
│   ✓ Reduce need for expensive chemical treatments                 │
│   ✓ Maximize yield and quality of harvest                        │
│   ✓ Lower overall farming costs                                   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 🌍 Market Opportunity

- **500M+** smallholder farmers worldwide need disease detection
- **$4.5B** addressable market in agricultural AI
- **30%** year-over-year growth in agritech sector

---

## 🔄 How It Works

AgriScan AI uses a multi-stage pipeline to process leaf images and provide disease predictions:

### Data Flow Pipeline

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Upload     │───►│   Preprocess │───►│   Predict    │───►│   Response   │
│   Image      │    │   (Resize,   │    │   (CNN       │    │   (Disease + │
│              │    │    Normalize)│    │   Inference) │    │   Treatment) │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
     1️⃣                2️⃣                3️⃣                4️⃣
```

### Step-by-Step Process

#### Step 1: Image Upload 📤
```
User Action          →  Frontend Processing        →  API Request
─────────────────────────────────────────────────────────────────────
• Capture photo      →  • File type validation     →  POST /api/predict
• Upload from device →  • Size check (<10MB)       →  multipart/form-data
• Drag & drop        →  • Preview generation       →  Image file
```

#### Step 2: Image Preprocessing ⚙️
```
Backend Processing   →  Tensor Processing           →  Ready for Model
─────────────────────────────────────────────────────────────────────
• Decode image      →  • Resize to 128×128         →  Shape: (128,128,3)
• Validate format   →  • Normalize pixels [0,1]    →  dtype: float32
• Error handling    →  • Expand dimensions        →  Shape: (1,128,128,3)
```

#### Step 3: Model Inference 🧠
```
Model Forward Pass   →  Probability Distribution   →  Class Prediction
─────────────────────────────────────────────────────────────────────
• Conv2D Block 1    →  [0.02, 0.75, 0.15, ...]    →  argmax → Class 1
• Conv2D Block 2    →  Softmax activation         →  Tomato Early Blight
• Conv2D Block 3    →  Output: 6 classes         →  Confidence: 75%
• Dense layers      →                             →
```

#### Step 4: Response Generation 📋
```
Prediction          →  Database Lookup            →  JSON Response
─────────────────────────────────────────────────────────────────────
• Class ID: 1       →  Treatment database         →  { "disease": "...", 
• Confidence: 75%   →  Disease details            →    "confidence": 75,
• Map to name      →  Severity, crop info        →    "treatment": "..." }
```

### End-to-End Request Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              REQUEST FLOW                                    │
└─────────────────────────────────────────────────────────────────────────────┘

  Client              Frontend            Backend             ML Service
    │                    │                   │                    │
    │  Select Image     │                   │                    │
    │───────────────────>│                   │                    │
    │                    │                   │                    │
    │                    │  POST /predict    │                    │
    │                    │──────────────────>│                    │
    │                    │                   │                    │
    │                    │                   │  Load & Preprocess │
    │                    │                   │───────────────────>│
    │                    │                   │                    │
    │                    │                   │        Model Inference
    │                    │                   │<───────────────────│
    │                    │                   │                    │
    │                    │  Response (JSON)  │                    │
    │                    │<──────────────────│                    │
    │                    │                   │                    │
    │  Display Results  │                   │                    │
    │<──────────────────│                   │                    │
    │                    │                   │                    │
```

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AGRI SCAN AI                                    │
│                         SYSTEM ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────┐      ┌────────────────────┐      ┌───────────────┐ │
│  │   CLIENT LAYER     │      │   SERVICE LAYER    │      │  DATA LAYER   │ │
│  │                    │      │                    │      │               │ │
│  │  ┌──────────────┐  │      │  ┌──────────────┐  │      │  ┌─────────┐  │ │
│  │  │   Web App    │  │      │  │  FastAPI     │  │      │  │  Model  │  │ │
│  │  │   (React)    │  │─────►│  │  Backend     │  │─────►│  │  Files  │  │ │
│  │  │  Port: 5173  │  │      │  │  Port: 8000  │  │      │  │  (.h5)  │  │ │
│  │  └──────────────┘  │      │  └──────────────┘  │      │  └─────────┘  │ │
│  │  ┌──────────────┐  │      │  ┌──────────────┐  │      │  ┌─────────┐  │ │
│  │  │ Mobile App   │  │      │  │   Uvicorn    │  │      │  │  JSON   │  │ │
│  │  │ (Future)     │  │      │  │   Server    │  │      │  │  Data   │  │ │
│  │  └──────────────┘  │      │  └──────────────┘  │      │  └─────────┘  │ │
│  └────────────────────┘      └────────────────────┘      └───────────────┘ │
│                                                                              │
│  ┌────────────────────┐      ┌────────────────────┐                            │
│  │  PRESENTATION     │      │   LOGIC LAYER     │                            │
│  │                    │      │                    │                            │
│  │  ┌──────────────┐  │      │  ┌──────────────┐  │                            │
│  │  │   Results   │  │      │  │ ML Service   │  │                            │
│  │  │   Display   │  │◄─────│  │  (TensorFlow)│  │                            │
│  │  │  - Disease  │  │      │  │  - Inference │  │                            │
│  │  │  - Conf. %  │  │      │  │  - Preprocess│  │                            │
│  │  │  - Treatment│  │      │  └──────────────┘  │                            │
│  │  └──────────────┘  │      │  ┌──────────────┐  │                            │
│  │  ┌──────────────┐  │      │  │ Treatment   │  │                            │
│  │  │  History     │  │      │  │  Service    │  │                            │
│  │  │  Tracking   │  │      │  │  (Database) │  │                            │
│  │  └──────────────┘  │      │  └──────────────┘  │                            │
│  └────────────────────┘      └────────────────────┘                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Layer | Responsibility | Technologies |
|------------|-------|----------------|--------------|
| **Frontend** | Presentation | User interface, image upload, results display | React 18, Vite, CSS3 |
| **Backend API** | Service | Request handling, validation, response formatting | FastAPI, Pydantic |
| **ML Service** | Logic | Model loading, inference, prediction | TensorFlow, Keras |
| **Treatment DB** | Data | Disease-to-treatment mapping | JSON, Python Dict |
| **Model Weights** | Data | Pre-trained CNN for classification | HDF5 (.h5) |

### Technology Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TECHNOLOGY INTERACTIONS                              │
└─────────────────────────────────────────────────────────────────────────────┘

    React + Vite                     FastAPI + Uvicorn                    TensorFlow
  ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
  │                 │   HTTP/JSON  │                 │   TF Model   │                 │
  │   User Actions  │─────────────►│   API Routes   │─────────────►│  ML Inference   │
  │                 │              │                 │              │                 │
  │ - Image Upload │◄────────────│  - /predict    │◄────────────│  - Load model   │
  │ - Results View │   Response   │  - /health     │   Prediction │  - Preprocess   │
  │ - History      │              │  - /classes    │              │  - Classify     │
  └─────────────────┘              └─────────────────┘              └─────────────────┘
         │                                │                                │
         │                                │                                │
         ▼                                ▼                                ▼
  ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
  │   Browser       │              │   Python App    │              │   GPU/CPU       │
  │   (Client)      │              │   (Server)      │              │   (Compute)     │
  └─────────────────┘              └─────────────────┘              └─────────────────┘
```

---

## 🧠 Model Architecture

### CNN Architecture Overview

The model is a custom Convolutional Neural Network (CNN) designed specifically for plant disease classification:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MODEL ARCHITECTURE                                   │
└─────────────────────────────────────────────────────────────────────────────┘

Input Layer
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONVOLUTIONAL BLOCK 1                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Conv2D(32 filters, 3×3 kernel)                                     │   │
│  │       ↓                                                              │   │
│  │  BatchNormalization                                                 │   │
│  │       ↓                                                              │   │
│  │  ReLU Activation                                                    │   │
│  │       ↓                                                              │   │
│  │  MaxPooling2D(2×2)                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONVOLUTIONAL BLOCK 2                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Conv2D(64 filters, 3×3 kernel)                                     │   │
│  │       ↓                                                              │   │
│  │  BatchNormalization                                                 │   │
│  │       ↓                                                              │   │
│  │  ReLU Activation                                                    │   │
│  │       ↓                                                              │   │
│  │  MaxPooling2D(2×2)                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONVOLUTIONAL BLOCK 3                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Conv2D(128 filters, 3×3 kernel)                                    │   │
│  │       ↓                                                              │   │
│  │  BatchNormalization                                                 │   │
│  │       ↓                                                              │   │
│  │  ReLU Activation                                                    │   │
│  │       ↓                                                              │   │
│  │  MaxPooling2D(2×2)                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONVOLUTIONAL BLOCK 4                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Conv2D(256 filters, 3×3 kernel)                                    │   │
│  │       ↓                                                              │   │
│  │  BatchNormalization                                                 │   │
│  │       ↓                                                              │   │
│  │  ReLU Activation                                                    │   │
│  │       ↓                                                              │   │
│  │  MaxPooling2D(2×2)                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
Flatten
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  DENSE BLOCK                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Dense(256 neurons) → Dropout(0.5) → Dense(128) → Dropout(0.3)     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
Output Layer (6 classes)
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Softmax                                                                  │
│  P(Healthy), P(Tomato Early Blight), P(Tomato Late Blight), ...          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Model Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Input Shape** | (128, 128, 3) | RGB image dimensions |
| **Image Size** | 128×128 pixels | Resized input |
| **Color Space** | RGB | Red, Green, Blue |
| **Normalization** | Pixel / 255.0 | Scale to [0, 1] |
| **Optimizer** | Adam | Adaptive moment estimation |
| **Learning Rate** | 0.001 | Default learning rate |
| **Loss Function** | Categorical Crossentropy | Multi-class classification |
| **Output Classes** | 6 | Number of disease classes |

### Layer Specifications

| Layer | Type | Filters/Kernel | Output Shape | Parameters |
|-------|------|----------------|--------------|------------|
| Input | InputLayer | - | (128, 128, 3) | 0 |
| Conv2D_1 | Conv2D | 32 × (3×3) | (128, 128, 32) | 896 |
| BatchNorm_1 | BatchNorm | - | (128, 128, 32) | 128 |
| MaxPool_1 | MaxPool2D | 2×2 | (64, 64, 32) | 0 |
| Conv2D_2 | Conv2D | 64 × (3×3) | (64, 64, 64) | 18,496 |
| BatchNorm_2 | BatchNorm | - | (64, 64, 64) | 256 |
| MaxPool_2 | MaxPool2D | 2×2 | (32, 32, 64) | 0 |
| Conv2D_3 | Conv2D | 128 × (3×3) | (32, 32, 128) | 73,856 |
| BatchNorm_3 | BatchNorm | - | (32, 32, 128) | 512 |
| MaxPool_3 | MaxPool2D | 2×2 | (16, 16, 128) | 0 |
| Conv2D_4 | Conv2D | 256 × (3×3) | (16, 16, 256) | 295,168 |
| BatchNorm_4 | BatchNorm | - | (16, 16, 256) | 1,024 |
| MaxPool_4 | MaxPool2D | 2×2 | (8, 8, 256) | 0 |
| Flatten | Flatten | - | (16384,) | 0 |
| Dense_1 | Dense | 256 | (256,) | 4,194,560 |
| Dropout_1 | Dropout | 0.5 | (256,) | 0 |
| Dense_2 | Dense | 128 | (128,) | 32,896 |
| Dropout_2 | Dropout | 0.3 | (128,) | 0 |
| Output | Dense | 6 (Softmax) | (6,) | 774 |
| **Total** | - | - | - | **4,618,470** |

### Model Performance Metrics

| Metric | Training | Validation | Test |
|--------|----------|------------|------|
| Accuracy | ~95% | ~90% | ~90% |
| Precision | ~94% | ~89% | ~88% |
| Recall | ~95% | ~90% | ~89% |
| F1-Score | ~94% | ~89% | ~88% |
| Inference Time | - | - | <500ms |

---

## 🦠 Supported Diseases

### Disease Classification Matrix

| ID | Disease Name | Crop | Pathogen | Severity | Color Code |
|----|--------------|------|----------|----------|------------|
| 0 | 🌿 Healthy | - | - | - | 🟢 Green |
| 1 | 🍅 Tomato Early Blight | Tomato | *Alternaria solani* | Medium | 🟡 Yellow |
| 2 | 🍅 Tomato Late Blight | Tomato | *Phytophthora infestans* | High | 🔴 Red |
| 3 | 🍅 Tomato Leaf Mold | Tomato | *Passalora fulva* | Low-Medium | 🟠 Orange |
| 4 | 🥔 Potato Early Blight | Potato | *Alternaria solani* | Medium | 🟡 Yellow |
| 5 | 🥔 Potato Late Blight | Potato | *Phytophthora infestans* | High | 🔴 Red |

### Detailed Disease Information

#### 0. Healthy 🌿
```json
{
  "id": 0,
  "name": "Healthy",
  "crop": null,
  "pathogen": null,
  "severity": "None",
  "treatment": "Plant is healthy. Continue regular care and monitoring."
}
```

#### 1. Tomato Early Blight 🍅
```json
{
  "id": 1,
  "name": "Tomato Early Blight",
  "crop": "Tomato",
  "pathogen": "Alternaria solani",
  "severity": "Medium",
  "symptoms": [
    "Dark brown spots with concentric rings (target-like)",
    "Lower leaves affected first",
    "Yellowing around spots",
    "Leaf drop in severe cases"
  ],
  "treatment": {
    "chemical": "Apply fungicide containing chlorothalonil or copper-based products",
    "cultural": [
      "Remove infected leaves",
      "Improve air circulation",
      "Avoid overhead watering",
      "Rotate crops"
    ],
    "prevention": "Use resistant varieties, maintain proper spacing"
  }
}
```

#### 2. Tomato Late Blight 🍅
```json
{
  "id": 2,
  "name": "Tomato Late Blight",
  "crop": "Tomato",
  "pathogen": "Phytophthora infestans",
  "severity": "High",
  "symptoms": [
    "Water-soaked dark spots on leaves",
    "White fuzzy growth on leaf undersides",
    "Rapidly spreading lesions",
    "Fruit rot with leathery texture"
  ],
  "treatment": {
    "chemical": "Apply fungicide immediately (metalaxyl, mancozeb)",
    "cultural": [
      "Remove and destroy infected plants",
      "Avoid overhead watering",
      "Improve drainage"
    ],
    "prevention": "Monitor weather, apply preventive fungicides in humid conditions"
  }
}
```

#### 3. Tomato Leaf Mold 🍅
```json
{
  "id": 3,
  "name": "Tomato Leaf Mold",
  "crop": "Tomato",
  "pathogen": "Passalora fulva",
  "severity": "Low-Medium",
  "symptoms": [
    "Yellow spots on upper leaf surface",
    "Olive-green to brown fuzzy growth undersides",
    "Leaf yellowing and drop",
    "Usually in humid conditions"
  ],
  "treatment": {
    "chemical": "Apply copper fungicide",
    "cultural": [
      "Reduce humidity",
      "Improve ventilation",
      "Remove infected leaves"
    ],
    "prevention": "Use resistant varieties, maintain low humidity"
  }
}
```

#### 4. Potato Early Blight 🥔
```json
{
  "id": 4,
  "name": "Potato Early Blight",
  "crop": "Potato",
  "pathogen": "Alternaria solani",
  "severity": "Medium",
  "symptoms": [
    "Dark brown to black spots",
    "Concentric ring pattern",
    "Older leaves affected first",
    "Tuber lesions (optional)"
  ],
  "treatment": {
    "chemical": "Apply chlorothalonil or mancozeb",
    "cultural": [
      "Rotate crops (2-3 years)",
      "Remove plant debris",
      "Adequate fertilization"
    ],
    "prevention": "Use certified seed, maintain good soil health"
  }
}
```

#### 5. Potato Late Blight 🥔
```json
{
  "id": 5,
  "name": "Potato Late Blight",
  "crop": "Potato",
  "pathogen": "Phytophthora infestans",
  "severity": "High",
  "symptoms": [
    "Water-soaked lesions",
    "White mold on leaf undersides",
    "Rapidly spreading",
    "Tuber rot (reddish-brown)"
  ],
  "treatment": {
    "chemical": "Apply fungicide immediately (metalaxyl, cymoxanil)",
    "cultural": [
      "Destroy infected tubers",
      "Use certified seed potatoes",
      "Hill up soil around plants"
    ],
    "prevention": "Monitor conditions, apply preventive fungicides"
  }
}
```

---

## 🛠️ Tech Stack

### Technology Overview

| Layer | Technology | Version | Purpose | Icon |
|-------|------------|---------|---------|------|
| **ML Framework** | TensorFlow | 2.15+ | Deep learning model training and inference | <img src="https://upload.wikimedia.org/wikipedia/commons/2/2d/Tensorflow_logo.svg" width="20"/> |
| **ML Wrapper** | Keras | 2.15+ | High-level neural network API | |
| **Backend** | FastAPI | 0.109+ | REST API framework | <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="20"/> |
| **Server** | Uvicorn | 0.27+ | ASGI server | |
| **Frontend** | React | 18+ | User interface | <img src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg" width="20"/> |
| **Build Tool** | Vite | 5+ | Frontend development and build | |
| **Container** | Docker | 24+ | Application containerization | <img src="https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png" width="20"/> |
| **Orchestration** | Docker Compose | 2+ | Multi-container deployment | |
| **Language (Backend)** | Python | 3.11+ | Backend development | <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width="20"/> |
| **Language (Frontend)** | JavaScript | ES6+ | Frontend development | |

### Development Dependencies

#### Backend Dependencies (`backend/requirements.txt`)
```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
tensorflow>=2.15.0
numpy>=1.26.0
pillow>=10.0.0
python-multipart>=0.0.6
pydantic>=2.5.0
pytest>=7.4.0
httpx>=0.26.0
```

#### Frontend Dependencies (`frontend/package.json`)
```
react>=18.2.0
react-dom>=18.2.0
vite>=5.0.0
```

---

## 📁 Project Structure

```
ai-crop-disease-detection/
│
├── 📂 backend/                      # FastAPI backend application
│   ├── 📂 app/
│   │   ├── 📂 api/                 # API endpoints
│   │   │   ├── routes.py           # Route definitions
│   │   │   └── dependencies.py    # Shared dependencies
│   │   ├── 📂 core/                # Core configuration
│   │   │   ├── config.py           # App settings
│   │   │   └── constants.py        # Constants
│   │   ├── 📂 models/              # Pydantic models
│   │   │   ├── schemas.py          # Request/Response schemas
│   │   │   └── entities.py         # Data entities
│   │   ├── 📂 services/            # Business logic
│   │   │   ├── ml_service.py       # ML model inference
│   │   │   └── treatment_service.py# Treatment database
│   │   └── 📂 utils/               # Utility functions
│   │       ├── image_processor.py  # Image preprocessing
│   │       └── validators.py       # Input validation
│   ├── 📂 tests/                   # Backend tests
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Backend container
│   └── main.py                     # Application entry point
│
├── 📂 frontend/                     # React frontend application
│   ├── 📂 src/
│   │   ├── 📂 components/          # React components
│   │   │   ├── ImageUploader.jsx   # Image upload component
│   │   │   ├── ResultsDisplay.jsx  # Results display
│   │   │   ├── LoadingSpinner.jsx  # Loading indicator
│   │   │   └── ErrorMessage.jsx    # Error handling
│   │   ├── 📂 services/            # API services
│   │   │   └── api.js              # API client
│   │   ├── 📂 hooks/               # React hooks
│   │   │   └── usePrediction.js    # Prediction hook
│   │   ├── App.jsx                 # Main application
│   │   ├── App.css                 # Application styles
│   │   └── main.jsx                # React entry point
│   ├── 📂 public/                   # Static assets
│   │   ├── index.html              # HTML template
│   │   └── favicon.ico             # Favicon
│   ├── package.json                # NPM dependencies
│   ├── vite.config.js              # Vite configuration
│   ├── Dockerfile                  # Frontend container
│   └── .env                        # Environment variables
│
├── 📂 ml/                           # Machine learning module
│   ├── 📂 model/                   # Trained model files
│   │   ├── plant_disease_model.h5 # Trained model weights
│   │   └── model_config.json       # Model configuration
│   ├── 📂 training/                # Training scripts
│   │   ├── train_model.py         # Main training script
│   │   ├── data_generator.py      # Data augmentation
│   │   ├── callbacks.py           # Training callbacks
│   │   └── evaluate.py            # Model evaluation
│   ├── 📂 inference/              # Inference utilities
│   │   ├── predict.py             # Prediction wrapper
│   │   └── preprocess.py         # Image preprocessing
│   └── 📂 notebooks/              # Jupyter notebooks
│       ├── EDA.ipynb              # Exploratory data analysis
│       └── Training.ipynb         # Training experiments
│
├── 📂 data/                        # Training and sample data
│   ├── 📂 train/                  # Training dataset
│   │   ├── Healthy/
│   │   ├── Tomato_Early_Blight/
│   │   ├── Tomato_Late_Blight/
│   │   ├── Tomato_Leaf_Mold/
│   │   ├── Potato_Early_Blight/
│   │   └── Potato_Late_Blight/
│   ├── 📂 val/                    # Validation dataset
│   └── 📂 test/                   # Test dataset
│
├── 📂 sample_images/               # Sample images for testing
│
├── 📂 tests/                       # Test files
│   ├── 📂 api/
│   │   ├── test_routes.py         # API route tests
│   │   └── test_integration.py    # Integration tests
│   └── 📂 ml/
│       ├── test_model.py          # Model tests
│       └── test_preprocessing.py # Preprocessing tests
│
├── 📂 docs/                        # Documentation
│   ├── api_docs.md               # API documentation
│   ├── model_docs.md            # Model documentation
│   ├── deployment.md            # Deployment guide
│   └── troubleshooting.md       # Troubleshooting guide
│
├── 📂 assets/                     # Project assets
│   ├── banner.png               # Project banner
│   └── logo.png                 # Project logo
│
├── 📂 .github/                   # GitHub workflows
│   └── workflows/
│       ├── ci.yml               # CI pipeline
│       └── deploy.yml           # CD pipeline
│
├── docker-compose.yml            # Docker Compose configuration
├── requirements.txt              # Root requirements
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
├── CHANGELOG.md                 # Version history
└── README.md                    # This file
```

---

## 🚀 Installation

### Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 18+ | Frontend development |
| Docker | 24+ | Container runtime |
| Docker Compose | 2+ | Container orchestration |
| RAM | 4GB+ | Model inference |

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/logeshkannan19/AI-Crop-Disease-Detection.git
cd AI-Crop-Disease-Detection

# Start all services
docker-compose up --build

# View logs
docker-compose logs -f
```

**Services Available:**
| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React web application |
| Backend API | http://localhost:8000 | FastAPI REST API |
| Swagger UI | http://localhost:8000/docs | Interactive API docs |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Model Configuration
MODEL_PATH=ml/model/plant_disease_model.h5
IMAGE_SIZE=128
MAX_FILE_SIZE=10485760  # 10MB

# Frontend Configuration
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=AgriScan AI
```

---

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api
```

### Endpoints Overview

| Method | Endpoint | Description | Status |
|--------|-----------|-------------|--------|
| GET | `/health` | Health check | ✅ Stable |
| POST | `/predict` | Predict disease | ✅ Stable |
| GET | `/classes` | Get supported classes | ✅ Stable |
| GET | `/treatments/{disease_id}` | Get treatment | ✅ Stable |

---

### 1. Health Check

**GET** `/health`

Check if the API is running and model is loaded.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/health
```

**Success Response (200):**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0",
  "uptime": "2026-04-08T00:00:00Z"
}
```

**Error Response (503):**
```json
{
  "status": "unhealthy",
  "model_loaded": false,
  "error": "Model failed to load"
}
```

---

### 2. Predict Disease

**POST** `/predict`

Predict disease from leaf image.

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/predict \
  -F "file=@path/to/leaf_image.jpg"
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | Image file (JPEG, PNG) |

**Success Response (200):**
```json
{
  "success": true,
  "disease": "Tomato_Early_Blight",
  "disease_id": 1,
  "confidence": 92.5,
  "treatment": "Apply fungicide containing chlorothalonil...",
  "crop": "Tomato",
  "severity": "Medium",
  "timestamp": "2026-04-08T12:00:00Z"
}
```

**Error Responses:**

| Status Code | Description |
|-------------|-------------|
| 400 | Invalid file format |
| 413 | File too large |
| 500 | Internal server error |

---

### 3. Get Supported Classes

**GET** `/classes`

Get list of all supported disease classes.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/classes
```

**Success Response (200):**
```json
{
  "count": 6,
  "classes": [
    {"id": 0, "name": "Healthy", "crop": null, "severity": "None"},
    {"id": 1, "name": "Tomato_Early_Blight", "crop": "Tomato", "severity": "Medium"},
    {"id": 2, "name": "Tomato_Late_Blight", "crop": "Tomato", "severity": "High"},
    {"id": 3, "name": "Tomato_Leaf_Mold", "crop": "Tomato", "severity": "Low-Medium"},
    {"id": 4, "name": "Potato_Early_Blight", "crop": "Potato", "severity": "Medium"},
    {"id": 5, "name": "Potato_Late_Blight", "crop": "Potato", "severity": "High"}
  ]
}
```

---

### 4. Get Treatment

**GET** `/treatments/{disease_id}`

Get detailed treatment information for a disease.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/treatments/1
```

**Success Response (200):**
```json
{
  "disease_id": 1,
  "name": "Tomato Early Blight",
  "crop": "Tomato",
  "pathogen": "Alternaria solani",
  "severity": "Medium",
  "symptoms": ["Dark brown spots with concentric rings", "Lower leaves affected"],
  "treatment": {
    "chemical": "Apply fungicide containing chlorothalonil or copper-based products",
    "cultural": ["Remove infected leaves", "Improve air circulation"],
    "prevention": "Use resistant varieties"
  }
}
```

---

### Interactive Documentation

| Tool | URL | Description |
|------|-----|-------------|
| **Swagger UI** | http://localhost:8000/docs | Interactive API explorer |
| **ReDoc** | http://localhost:8000/redoc | Alternative documentation |

---

## 🎓 Model Training

### Training Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Image Size | 128×128 pixels | Input dimensions |
| Batch Size | 32 | Training batch size |
| Epochs | 20 | Number of training epochs |
| Validation Split | 20% | Training/validation split |
| Optimizer | Adam | Adaptive moment estimation |
| Learning Rate | 0.001 | Default learning rate |
| Loss | Categorical Crossentropy | Multi-class loss |

### Training Commands

```bash
cd ml/training
python train_model.py
```

### Training Data Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Raw Data  │───►│  Preprocess │───►│   Augment   │───►│   Train     │
│   (Images)  │    │   (Resize)  │    │   (Random)  │    │   (CNN)     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Expected Performance

| Metric | Training | Validation | Test |
|--------|----------|------------|------|
| Accuracy | ~95% | ~90% | ~90% |
| Precision | ~94% | ~89% | ~88% |
| Recall | ~95% | ~90% | ~89% |
| F1-Score | ~94% | ~89% | ~88% |
| Inference Time | - | - | <500ms |
| Model Size | - | - | ~15MB |

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Test Coverage

| Category | Tests |
|----------|-------|
| API Routes | Endpoint validation, error handling |
| Model | Loading verification, inference |
| Preprocessing | Image resize, normalization |
| Integration | End-to-end workflow |

---

## 💼 Business Model

### Pricing Tiers

| Tier | Features | Price | Target |
|------|----------|-------|--------|
| 🆓 **Freemium** | 10 scans/month, basic detection | Free | Individual farmers |
| ⭐ **Premium** | Unlimited scans, history, treatments | $4.99/mo | Small farms |
| 🏢 **Enterprise** | API access, analytics, custom integration | Custom | Cooperatives, companies |

### Revenue Streams

1. 💳 **Subscription Revenue** - Monthly/annual Premium subscriptions
2. 🔌 **API Access** - Enterprise API pricing
3. 🎨 **White-label** - Custom branded solutions

### Target Market

| Segment | Size | Opportunity |
|---------|------|-------------|
| Smallholder farmers | 500M+ | Disease detection |
| Agricultural cooperatives | 100K+ | Bulk access |
| Farm management | 10K+ | Integration |
| Research institutions | 5K+ | Data services |

---

## 🗺️ Future Roadmap

### Phase 2 (Q3 2026)
- [ ] Add 10+ crop types (Apple, Grape, Corn, Wheat, etc.)
- [ ] Implement TensorFlow.js for offline mode
- [ ] Mobile app (iOS/Android)

### Phase 3 (Q4 2026)
- [ ] Multi-language support (Spanish, French, Hindi)
- [ ] Drone imagery integration
- [ ] Batch processing API

### Phase 4 (2027)
- [ ] Disease severity assessment
- [ ] Yield prediction modeling
- [ ] Integration with farm management systems

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎉 Open a Pull Request

### Development Guidelines

| Rule | Description |
|------|-------------|
| Code Style | Follow PEP 8 (Python), ESLint (JS) |
| Documentation | Add docstrings to functions |
| Testing | Write tests for new features |
| Commits | Use meaningful commit messages |

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

| Resource | Description | Link |
|----------|-------------|------|
| **PlantVillage Dataset** | Training data | [Kaggle](https://www.kaggle.com/datasets/abdallahalomari/plantvillage-dataset) |
| **TensorFlow** | ML Framework | [Website](https://tensorflow.org/) |
| **FastAPI** | Backend Framework | [Website](https://fastapi.tiangolo.com/) |
| **React** | Frontend Framework | [Website](https://react.dev/) |
| **EACE 2026** | Exhibition | [Website](https://eace.org/) |

---

## 📞 Contact

| Channel | Contact |
|---------|---------|
| 📧 **Email** | hello@agriscan.ai |
| 🐙 **GitHub** | [logeshkannan19/AI-Crop-Disease-Detection](https://github.com/logeshkannan19/AI-Crop-Disease-Detection) |
| 💼 **LinkedIn** | [AgriScan AI](https://linkedin.com/company/agriscan-ai) |
| 🐦 **Twitter** | [@AgriScanAI](https://twitter.com/AgriScanAI) |

---

<div align="center">

**Built with ❤️ for sustainable agriculture**

[![GitHub stars](https://img.shields.io/github/stars/logeshkannan19/AI-Crop-Disease-Detection?style=social)](https://github.com/logeshkannan19/AI-Crop-Disease-Detection)
[![GitHub forks](https://img.shields.io/github/forks/logeshkannan19/AI-Crop-Disease-Detection?style=social)](https://github.com/logeshkannan19/AI-Crop-Disease-Detection)

</div>