from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from passlib.hash import bcrypt
import secrets

app = FastAPI(title="Catholic Social Network API", version="0.1.0")


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    display_name: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str
    display_name: str


class PostRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)


class Post(BaseModel):
    id: int
    author: str
    content: str


class FeedResponse(BaseModel):
    posts: List[Post]


_users: Dict[str, Dict[str, str]] = {}
_sessions: Dict[str, str] = {}
_posts: List[Dict[str, str]] = []


def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.replace("Bearer", "").strip()
    username = _sessions.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username


@app.post("/register", response_model=AuthResponse, status_code=201)
def register(payload: RegisterRequest):
    username = payload.username.lower()
    if username in _users:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = bcrypt.hash(payload.password)
    _users[username] = {"display_name": payload.display_name, "password": hashed}

    token = secrets.token_urlsafe(24)
    _sessions[token] = username
    return AuthResponse(token=token, display_name=payload.display_name)


@app.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):
    username = payload.username.lower()
    user = _users.get(username)
    if not user or not bcrypt.verify(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_urlsafe(24)
    _sessions[token] = username
    return AuthResponse(token=token, display_name=user["display_name"])


@app.post("/posts", response_model=Post, status_code=201)
def create_post(payload: PostRequest, current_user: str = Depends(get_current_user)):
    post_id = len(_posts) + 1
    post = {"id": post_id, "author": _users[current_user]["display_name"], "content": payload.content}
    _posts.insert(0, post)
    return Post(**post)


@app.get("/feed", response_model=FeedResponse)
def feed() -> FeedResponse:
    return FeedResponse(posts=[Post(**post) for post in _posts])


@app.get("/health")
def health():
    return {"status": "ok"}
