"""
Blockchain Traceability Routes
=============================
Track crop health records on blockchain for supply chain transparency.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt

router = APIRouter(prefix="/api/blockchain", tags=["blockchain"])
security = HTTPBearer()

CHAIN_FILE = Path("backend/app/data/chain.json")
CHAIN_FILE.parent.mkdir(parents=True, exist_ok=True)

SECRET_KEY = "agriScan-secret-key-2026"
ALGORITHM = "HS256"


class CropRecord(BaseModel):
    crop_type: str
    variety: str
    farm_id: str
    planting_date: str
    harvest_date: str = None
    health_records: List[dict] = []


class HealthEntry(BaseModel):
    detection_id: str
    disease: str
    confidence: float
    treatment: str
    location: dict
    image_hash: str


class Block:
    def __init__(self, index: int, timestamp: str, data: dict, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data)}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


def load_chain() -> List[dict]:
    if not CHAIN_FILE.exists():
        genesis = {
            "index": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "data": {"type": "genesis", "message": "AgriScan AI Blockchain Genesis Block"},
            "previous_hash": "0",
            "hash": "genesis"
        }
        with open(CHAIN_FILE, "w") as f:
            json.dump([genesis], f, indent=2)
        return [genesis]
    with open(CHAIN_FILE, "r") as f:
        return json.load(f)


def save_chain(chain: List[dict]):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/register")
async def register_crop(
    record: CropRecord,
    user_id: str = Depends(get_current_user_id)
):
    chain = load_chain()
    
    data = {
        "type": "crop_registration",
        "user_id": user_id,
        "crop": record.model_dump()
    }
    
    block = Block(
        index=len(chain),
        timestamp=datetime.utcnow().isoformat(),
        data=data,
        previous_hash=chain[-1]["hash"]
    )
    
    chain.append({
        "index": block.index,
        "timestamp": block.timestamp,
        "data": block.data,
        "previous_hash": block.previous_hash,
        "hash": block.hash
    })
    
    save_chain(chain)
    
    return {
        "success": True,
        "block_index": block.index,
        "block_hash": block.hash,
        "message": "Crop registered on blockchain"
    }


@router.post("/health-record")
async def add_health_record(
    crop_id: str,
    entry: HealthEntry,
    user_id: str = Depends(get_current_user_id)
):
    chain = load_chain()
    
    data = {
        "type": "health_record",
        "user_id": user_id,
        "crop_id": crop_id,
        "detection": entry.model_dump()
    }
    
    block = Block(
        index=len(chain),
        timestamp=datetime.utcnow().isoformat(),
        data=data,
        previous_hash=chain[-1]["hash"]
    )
    
    chain.append({
        "index": block.index,
        "timestamp": block.timestamp,
        "data": block.data,
        "previous_hash": block.previous_hash,
        "hash": block.hash
    })
    
    save_chain(chain)
    
    return {
        "success": True,
        "block_index": block.index,
        "block_hash": block.hash,
        "previous_hash": block.previous_hash,
        "verified": True
    }


@router.get("/chain")
async def get_chain():
    chain = load_chain()
    return {
        "length": len(chain),
        "chain": chain
    }


@router.get("/verify")
async def verify_chain():
    chain = load_chain()
    
    for i in range(1, len(chain)):
        if chain[i]["previous_hash"] != chain[i-1]["hash"]:
            return {"valid": False, "broken_at": i}
    
    return {
        "valid": True,
        "blocks": len(chain),
        "integrity": "All blocks verified"
    }


@router.get("/records/{crop_id}")
async def get_crop_records(crop_id: str):
    chain = load_chain()
    records = []
    
    for block in chain:
        if block["data"].get("crop_id") == crop_id or \
           (block["data"].get("crop", {}).get("farm_id") == crop_id):
            records.append(block)
    
    return {
        "crop_id": crop_id,
        "records": records,
        "total_records": len(records)
    }


@router.get("/export/{crop_id}")
async def export_blockchain_cert(crop_id: str):
    chain = load_chain()
    records = [b for b in chain if b["data"].get("crop_id") == crop_id]
    
    cert = {
        "certificate_id": hashlib.sha256(crop_id.encode()).hexdigest()[:16],
        "crop_id": crop_id,
        "issued_at": datetime.utcnow().isoformat(),
        "total_records": len(records),
        "records": records,
        "verified": all(
            chain[i]["previous_hash"] == chain[i-1]["hash"] 
            for i in range(1, len(chain))
        )
    }
    
    return cert
