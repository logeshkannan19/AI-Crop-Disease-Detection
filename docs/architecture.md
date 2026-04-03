# AgriScan AI - Architecture Documentation

## System Overview

AgriScan AI is an end-to-end AI-powered crop disease detection system designed for farmers and agricultural businesses.

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Frontend)                        │
│   React Web App → Upload Image → Display Results               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND (API)                           │
│   FastAPI Server → Handle Requests → Return JSON               │
│   - /api/health     - Health check                             │
│   - /api/predict    - Disease prediction                       │
│   - /api/classes    - Get supported classes                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ML SERVICE (Inference)                      │
│   DiseaseClassifier → Load Model → Predict Disease             │
│   - Preprocess image                                            │
│   - Run CNN inference                                           │
│   - Return disease + treatment                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         ML MODEL                                │
│   Keras CNN Model (plant_disease_model.keras)                  │
│   - Input: 128x128 RGB image                                    │
│   - Output: 6 class probabilities                               │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (React + Vite)
- **Location**: `frontend/`
- **Port**: 5173 (dev), 3000 (prod)
- **Features**:
  - Image upload with drag-and-drop
  - Preview selected image
  - Display prediction results
  - Show confidence percentage
  - Treatment recommendations

### Backend (FastAPI)
- **Location**: `backend/app/`
- **Port**: 8000
- **Structure**:
  ```
  backend/app/
  ├── api/          # API routes
  │   └── prediction.py
  ├── core/         # Configuration
  │   ├── config.py
  │   └── logging.py
  ├── models/       # Data schemas
  │   └── schemas.py
  ├── services/     # Business logic
  │   └── ml_service.py
  └── main.py       # Entry point
  ```

### ML Module
- **Training**: `ml/training/train_model.py`
- **Inference**: `ml/inference/inference.py`
- **Model**: `ml/model/plant_disease_model.keras`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/api/health` | Health check |
| POST | `/api/predict` | Predict disease |
| GET | `/api/classes` | Get supported classes |

## Environment Variables

See `.env.example` for configuration options:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `MODEL_PATH`: Path to trained model
- `UPLOAD_DIR`: Upload directory path
- `LOG_LEVEL`: Logging level

## Deployment

### Docker
```bash
# Build and run
docker-compose up --build
```

### Manual
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn backend.app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```