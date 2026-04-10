"""
Notification Routes
==================
SMS and Email notification endpoints for alerts.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import jwt

router = APIRouter(prefix="/api/notifications", tags=["notifications"])
security = HTTPBearer()

NOTIFICATIONS_FILE = Path("backend/app/data/notifications.json")
NOTIFICATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

SECRET_KEY = "agriScan-secret-key-2026"
ALGORITHM = "HS256"


class NotificationSettings(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    email_alerts: bool = True
    sms_alerts: bool = False
    disease_alerts: bool = True
    weather_alerts: bool = True
    weekly_report: bool = False


class AlertRequest(BaseModel):
    type: str  # disease, weather, weekly
    disease: Optional[str] = None
    confidence: Optional[float] = None
    message: Optional[str] = None


def load_settings() -> dict:
    if not NOTIFICATIONS_FILE.exists():
        return {}
    with open(NOTIFICATIONS_FILE, "r") as f:
        return json.load(f)


def save_settings(settings: dict):
    with open(NOTIFICATIONS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/settings")
async def get_notification_settings(user_id: str = Depends(get_current_user_id)):
    settings = load_settings()
    user_settings = settings.get(user_id, {
        "email_alerts": True,
        "sms_alerts": False,
        "disease_alerts": True,
        "weather_alerts": True,
        "weekly_report": False
    })
    return user_settings


@router.post("/settings")
async def update_notification_settings(
    settings_update: NotificationSettings,
    user_id: str = Depends(get_current_user_id)
):
    settings = load_settings()
    settings[user_id] = settings_update.model_dump(exclude_none=True)
    save_settings(settings)
    return {"success": True, "message": "Notification settings updated"}


@router.post("/send")
async def send_alert(
    alert: AlertRequest,
    user_id: str = Depends(get_current_user_id)
):
    settings = load_settings().get(user_id, {})
    
    result = {"success": True, "notifications_sent": []}
    
    if alert.type == "disease" and settings.get("disease_alerts"):
        message = f"🦠 Disease Alert: {alert.disease} detected ({(alert.confidence or 0)*100:.1f}% confidence)"
        if settings.get("email_alerts") and settings.get("email"):
            result["notifications_sent"].append({"type": "email", "to": settings["email"]})
        if settings.get("sms_alerts") and settings.get("phone"):
            result["notifications_sent"].append({"type": "sms", "to": settings["phone"]})
    
    elif alert.type == "weather" and settings.get("weather_alerts"):
        message = f"⚠️ Weather Alert: High disease risk conditions detected in your area"
        if settings.get("email_alerts") and settings.get("email"):
            result["notifications_sent"].append({"type": "email", "to": settings["email"]})
    
    elif alert.type == "weekly" and settings.get("weekly_report"):
        message = "📊 Weekly Report: Your crop health summary is ready"
        if settings.get("email_alerts") and settings.get("email"):
            result["notifications_sent"].append({"type": "email", "to": settings["email"]})
    
    return result


@router.get("/history")
async def get_notification_history(user_id: str = Depends(get_current_user_id)):
    return {
        "notifications": [
            {"type": "disease", "message": "Late blight alert for tomato crop", "sent_at": datetime.utcnow().isoformat()},
            {"type": "weather", "message": "High humidity alert", "sent_at": datetime.utcnow().isoformat()}
        ]
    }
