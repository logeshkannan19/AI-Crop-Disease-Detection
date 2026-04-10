"""
Community Forum Routes
======================
Farmers community discussions and knowledge sharing.
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt

router = APIRouter(prefix="/api/forum", tags=["forum"])
security = HTTPBearer()

POSTS_FILE = Path("backend/app/data/forum_posts.json")
USERS_FILE = Path("backend/app/data/forum_users.json")
POSTS_FILE.parent.mkdir(parents=True, exist_ok=True)

SECRET_KEY = "agriScan-secret-key-2026"
ALGORITHM = "HS256"


class PostCreate(BaseModel):
    title: str
    content: str
    category: str  # discussion, question, tip, success_story
    crop: Optional[str] = None
    tags: List[str] = []


class CommentCreate(BaseModel):
    content: str


def load_posts() -> List[dict]:
    if not POSTS_FILE.exists():
        return []
    with open(POSTS_FILE, "r") as f:
        return json.load(f)


def save_posts(posts: List[dict]):
    with open(POSTS_FILE, "w") as f:
        json.dump(posts, f, indent=2)


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/posts")
async def get_posts(
    category: Optional[str] = None,
    crop: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    posts = load_posts()
    
    if category:
        posts = [p for p in posts if p["category"] == category]
    if crop:
        posts = [p for p in posts if p.get("crop") == crop]
    if search:
        search = search.lower()
        posts = [p for p in posts if search in p["title"].lower() or search in p["content"].lower()]
    
    posts.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {
        "posts": posts[offset:offset+limit],
        "total": len(posts),
        "offset": offset,
        "limit": limit
    }


@router.post("/posts")
async def create_post(
    post: PostCreate,
    user_id: str = Depends(get_current_user_id)
):
    posts = load_posts()
    
    new_post = {
        "id": str(uuid.uuid4()),
        "author_id": user_id,
        "author_name": "Farmer",  # Would get from user DB
        "title": post.title,
        "content": post.content,
        "category": post.category,
        "crop": post.crop,
        "tags": post.tags,
        "likes": 0,
        "comments": [],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    posts.insert(0, new_post)
    save_posts(posts)
    
    return {
        "success": True,
        "post_id": new_post["id"]
    }


@router.get("/posts/{post_id}")
async def get_post(post_id: str):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/posts/{post_id}/like")
async def like_post(post_id: str, user_id: str = Depends(get_current_user_id)):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post["likes"] = post.get("likes", 0) + 1
    save_posts(posts)
    
    return {"success": True, "likes": post["likes"]}


@router.post("/posts/{post_id}/comments")
async def add_comment(
    post_id: str,
    comment: CommentCreate,
    user_id: str = Depends(get_current_user_id)
):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    new_comment = {
        "id": str(uuid.uuid4()),
        "author_id": user_id,
        "author_name": "Farmer",
        "content": comment.content,
        "created_at": datetime.utcnow().isoformat()
    }
    
    post.setdefault("comments", []).append(new_comment)
    save_posts(posts)
    
    return {
        "success": True,
        "comment_id": new_comment["id"]
    }


@router.delete("/posts/{post_id}")
async def delete_post(post_id: str, user_id: str = Depends(get_current_user_id)):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post["author_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    posts = [p for p in posts if p["id"] != post_id]
    save_posts(posts)
    
    return {"success": True}


@router.get("/categories")
async def get_categories():
    return {
        "categories": [
            {"id": "discussion", "name": "General Discussion", "icon": "💬", "count": 45},
            {"id": "question", "name": "Questions & Help", "icon": "❓", "count": 32},
            {"id": "tip", "name": "Farming Tips", "icon": "💡", "count": 28},
            {"id": "success_story", "name": "Success Stories", "icon": "🏆", "count": 15}
        ],
        "crops": [
            {"id": "Tomato", "icon": "🍅", "count": 35},
            {"id": "Potato", "icon": "🥔", "count": 28},
            {"id": "Corn", "icon": "🌽", "count": 22},
            {"id": "Wheat", "icon": "🌾", "count": 18},
            {"id": "Rice", "icon": "🍚", "count": 12}
        ]
    }


@router.get("/trending")
async def get_trending_posts():
    posts = load_posts()
    trending = sorted(posts, key=lambda x: x.get("likes", 0) + len(x.get("comments", [])) * 2, reverse=True)[:5]
    return {"posts": trending}
