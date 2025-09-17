from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.services.user_service import init_db
from typing import Optional
import uvicorn

app = FastAPI(
    title="AI Coach Backend",
    description="Provides meal and workout plans using LLMs based on user profile and preferences.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SQLite DB
init_db()

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User models (simplified)
class UserCreate(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

# In-memory user store for demo (replace with DB logic)
fake_users_db = {}

@app.get("/")
def read_root():
    return {"message": "AI Coach API is running."}

@app.post("/signup")
def signup(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_users_db[user.email] = {"password": user.password, "first_name": user.first_name, "last_name": user.last_name}
    return {"message": "User registered successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # TODO: Return JWT token
    return {"access_token": form_data.username, "token_type": "bearer"}

@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    # TODO: Implement token blacklist or session invalidation
    return {"message": "Logged out"}

# CRUD endpoints for users (to be implemented)
# TODO: Import and include user_routes router when implemented

# LLM prompt endpoint
class PromptRequest(BaseModel):
    user_profile: dict
    prompt_type: str  # "meal" or "workout"

@app.post("/generate_plan")
def generate_plan(request: PromptRequest):
    # TODO: Call LLM client with user_profile and prompt_type
    return {"plan": "Generated plan will appear here."}

# TODO: Add endpoints for user history retrieval and storage

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)