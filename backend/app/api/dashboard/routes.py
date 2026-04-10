"""
Dashboard Routes
================
Analytics and detection history endpoints.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
security = HTTPBearer()

HISTORY_FILE = Path("backend/app/data/detection_history.json")
HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

SECRET_KEY = "agriScan-secret-key-2026"
ALGORITHM = "HS256"


def load_history() -> list:
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history: list):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/record")
async def record_detection(
    user_id: str = Depends(get_current_user_id),
    disease: str = None,
    confidence: float = None
):
    history = load_history()
    
    record = {
        "id": len(history) + 1,
        "user_id": user_id,
        "disease": disease,
        "confidence": confidence,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    history.append(record)
    save_history(history)
    
    return {"success": True}


@router.get("/stats")
async def get_stats(user_id: str = Depends(get_current_user_id)):
    history = load_history()
    user_history = [h for h in history if h.get("user_id") == user_id]
    
    total = len(user_history)
    healthy = len([h for h in user_history if h.get("disease") == "Healthy"])
    diseased = total - healthy
    
    confidences = [h.get("confidence", 0) for h in user_history if h.get("confidence")]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    disease_counts = Counter([h.get("disease") for h in user_history])
    
    return {
        "total_scans": total,
        "healthy_count": healthy,
        "diseased_count": diseased,
        "avg_confidence": round(avg_confidence * 100, 1),
        "disease_breakdown": dict(disease_counts),
        "recent": user_history[-10:] if user_history else []
    }


@router.get("/history")
async def get_history(
    limit: int = 50,
    user_id: str = Depends(get_current_user_id)
):
    history = load_history()
    user_history = [h for h in history if h.get("user_id") == user_id]
    return user_history[-limit:]


@router.get("/trends")
async def get_trends(
    days: int = 7,
    user_id: str = Depends(get_current_user_id)
):
    history = load_history()
    user_history = [h for h in history if h.get("user_id") == user_id]
    
    cutoff = datetime.utcnow() - timedelta(days=days)
    recent = [h for h in user_history if datetime.fromisoformat(h["timestamp"]) > cutoff]
    
    daily_stats = {}
    for h in recent:
        date = datetime.fromisoformat(h["timestamp"]).strftime("%Y-%m-%d")
        if date not in daily_stats:
            daily_stats[date] = {"total": 0, "healthy": 0, "diseased": 0}
        daily_stats[date]["total"] += 1
        if h.get("disease") == "Healthy":
            daily_stats[date]["healthy"] += 1
        else:
            daily_stats[date]["diseased"] += 1
    
    return {
        "days": days,
        "daily": daily_stats
    }
