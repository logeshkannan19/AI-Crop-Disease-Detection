# AgriScan AI - API Documentation

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Root

**GET** `/`

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

---

### 2. Health Check

**GET** `/api/health`

Check if the service is running and model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0"
}
```

---

### 3. Predict Disease

**POST** `/api/predict`

Predict disease from a plant leaf image.

**Content-Type:** `multipart/form-data`

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
  "treatment": "Apply fungicide containing chlorothalonil...",
  "top_predictions": [
    {"disease": "Tomato_Early_Blight", "confidence": 0.925},
    {"disease": "Tomato_Late_Blight", "confidence": 0.052},
    {"disease": "Potato_Early_Blight", "confidence": 0.015}
  ]
}
```

**Error Responses:**

| Status Code | Description |
|-------------|-------------|
| 400 | Invalid file type or no file provided |
| 413 | File too large |
| 500 | Internal server error |

---

### 4. Get Classes

**GET** `/api/classes`

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
    "Healthy": "Plant is healthy! ...",
    "Tomato_Early_Blight": "Apply fungicide ...",
    ...
  }
}
```

---

## Example Usage

### Using cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Predict disease
curl -X POST -F "file=@leaf_image.jpg" http://localhost:8000/api/predict

# Get classes
curl http://localhost:8000/api/classes
```

### Using Python

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

### Using JavaScript

```javascript
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://localhost:8000/api/predict', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result.disease, result.confidence);
```

---

## Supported Classes

| Class ID | Name | Description |
|----------|------|-------------|
| 0 | Healthy | No disease detected |
| 1 | Tomato_Early_Blight | Alternaria solani |
| 2 | Tomato_Late_Blight | Phytophthora infestans |
| 3 | Tomato_Leaf_Mold | Passalora fulva |
| 4 | Potato_Early_Blight | Alternaria solani |
| 5 | Potato_Late_Blight | Phytophthora infestans |

---

## Rate Limits

Currently no rate limits. Production deployment should include rate limiting.

---

## Error Handling

All errors return a JSON response:

```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```