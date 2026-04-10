"""
Expert Consultation Routes
==========================
Connect users with agricultural experts.
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt

router = APIRouter(prefix="/api/expert", tags=["expert"])
security = HTTPBearer()

EXPERT_FILE = Path("backend/app/data/experts.json")
CONSULT_FILE = Path("backend/app/data/consultations.json")
EXPERT_FILE.parent.mkdir(parents=True, exist_ok=True)

SECRET_KEY = "agriScan-secret-key-2026"
ALGORITHM = "HS256"


class Expert(BaseModel):
    id: str
    name: str
    specialization: str
    experience: int
    rating: float
    consultations: int
    available: bool
    languages: List[str]
    hourly_rate: float


class ConsultationRequest(BaseModel):
    expert_id: str
    disease: str
    crop: str
    description: str
    urgency: str = "normal"


class ExpertResponse(BaseModel):
    id: str
    expert_id: str
    user_id: str
    message: str
    timestamp: str
    read: bool


def load_experts() -> List[dict]:
    if not EXPERT_FILE.exists():
        return [
            {"id": "exp1", "name": "Dr. Rajesh Kumar", "specialization": "Tomato & Potato Diseases", "experience": 15, "rating": 4.8, "consultations": 234, "available": True, "languages": ["English", "Hindi"], "hourly_rate": 25},
            {"id": "exp2", "name": "Dr. Maria Santos", "specialization": "Fruit Trees & Grapes", "experience": 12, "rating": 4.9, "consultations": 189, "available": True, "languages": ["English", "Spanish"], "hourly_rate": 30},
            {"id": "exp3", "name": "Dr. Wei Chen", "specialization": "Rice & Wheat", "experience": 20, "rating": 4.7, "consultations": 312, "available": True, "languages": ["English", "Chinese"], "hourly_rate": 35},
            {"id": "exp4", "name": "Dr. John Smith", "specialization": "Corn & General Crops", "experience": 18, "rating": 4.6, "consultations": 156, "available": False, "languages": ["English"], "hourly_rate": 28}
        ]
    with open(EXPERT_FILE, "r") as f:
        return json.load(f)


def load_consultations() -> List[dict]:
    if not CONSULT_FILE.exists():
        return []
    with open(CONSULT_FILE, "r") as f:
        return json.load(f)


def save_consultations(consultations: List[dict]):
    with open(CONSULT_FILE, "w") as f:
        json.dump(consultations, f, indent=2)


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/experts")
async def get_experts(specialization: Optional[str] = None):
    experts = load_experts()
    if specialization:
        experts = [e for e in experts if specialization.lower() in e["specialization"].lower()]
    return {"experts": experts}


@router.get("/experts/{expert_id}")
async def get_expert(expert_id: str):
    experts = load_experts()
    expert = next((e for e in experts if e["id"] == expert_id), None)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    return expert


@router.post("/consult")
async def request_consultation(
    request: ConsultationRequest,
    user_id: str = Depends(get_current_user_id)
):
    consultations = load_consultations()
    
    consultation = {
        "id": str(uuid.uuid4()),
        "expert_id": request.expert_id,
        "user_id": user_id,
        "disease": request.disease,
        "crop": request.crop,
        "description": request.description,
        "urgency": request.urgency,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "messages": []
    }
    
    consultations.append(consultation)
    save_consultations(consultations)
    
    return {
        "success": True,
        "consultation_id": consultation["id"],
        "message": "Consultation request submitted. Expert will respond within 24 hours."
    }


@router.get("/consultations")
async def get_my_consultations(user_id: str = Depends(get_current_user_id)):
    consultations = load_consultations()
    user_consultations = [
        c for c in consultations 
        if c["user_id"] == user_id or c["expert_id"] == user_id
    ]
    return {"consultations": user_consultations}


@router.get("/consultations/{consultation_id}")
async def get_consultation(consultation_id: str, user_id: str = Depends(get_current_user_id)):
    consultations = load_consultations()
    consultation = next((c for c in consultations if c["id"] == consultation_id), None)
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    if consultation["user_id"] != user_id and consultation["expert_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return consultation


@router.post("/consultations/{consultation_id}/message")
async def send_message(
    consultation_id: str,
    message: str,
    user_id: str = Depends(get_current_user_id)
):
    consultations = load_consultations()
    consultation = next((c for c in consultations if c["id"] == consultation_id), None)
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    consultation["messages"].append({
        "id": str(uuid.uuid4()),
        "sender": user_id,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "read": False
    })
    
    save_consultations(consultations)
    return {"success": True}
