# AgriScan AI - Demo Guide

## Exhibition Demo Script

Use this guide for EACE 2026 exhibition demonstrations.

### Demo Flow (5 minutes)

#### 1. Introduction (30 seconds)
> "Welcome to AgriScan AI! We're solving a $220 billion problem - plant diseases destroy 40% of global crops annually. Our AI system detects diseases in seconds using just a phone camera."

#### 2. Problem Context (30 seconds)
- Show statistics:
  - 40% crop loss to diseases
  - Small farmers most vulnerable
  - Early detection saves 80% of affected crops

#### 3. Live Demo (2 minutes)

**Step 1: Upload**
- Show the web interface
- Click upload or drag image

**Step 2: Analysis**
- Point to the "Analyzing..." state
- Explain the CNN model processing

**Step 3: Results**
- Show disease diagnosis
- Point out confidence percentage
- Read treatment recommendation

#### 4. Technology Stack (1 minute)
> "We use TensorFlow for the CNN model, FastAPI for the backend, and React for the frontend. The model achieves 90%+ accuracy."

#### 5. Business Model (1 minute)
- Freemium: Free basic, $4.99/mo premium
- B2B: Enterprise pricing
- Target: 500M+ smallholder farmers

### Quick Start for Demo

#### Option 1: Docker (Recommended)
```bash
# Start everything
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

#### Option 2: Manual
```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
uvicorn backend.app.main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm install
npm run dev
```

### Test Images

Place test images in `sample_images/`:
- healthy_tomato.jpg
- early_blight.jpg
- late_blight.jpg
- leaf_mold.jpg

### Sample Output

**Input:** Leaf image of infected tomato

**Output:**
```json
{
  "success": true,
  "disease": "Tomato_Early_Blight",
  "confidence": 92.5,
  "treatment": "Apply fungicide containing chlorothalonil..."
}
```

### Demo Talking Points

1. **Speed**: "Results in under 2 seconds"
2. **Accuracy**: "90%+ accuracy on test data"
3. **Affordability**: "10x cheaper than lab testing"
4. **Accessibility**: "Works on any smartphone"
5. **Impact**: "Can save 80% of affected crops"

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check Python 3.11+, install requirements |
| Frontend won't load | Run `npm install`, check port 5173 |
| API returns error | Check model file exists in ml/model/ |
| CORS error | Update CORS_ORIGINS in .env |

### Contact for Follow-up

- Email: hello@agriscan.ai
- Website: agriscan.ai (placeholder)
- GitHub: github.com/agriscan-ai

---

*Thank you for your interest in AgriScan AI!*