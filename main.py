import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

security = HTTPBearer()

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    response = supabase.auth.get_user(token)

    if not response.user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return response.user

app = FastAPI(
    title="Task API Auth",
    description="FastAPI authentication API using Supabase Auth.",
    version="1.0"
)

class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    response = supabase.auth.sign_in_with_password({
        "email": data.email,
        "password": data.password
    })

    return {
        "message": "Login successful",
        "access_token": response.session.access_token,
        "token_type": "bearer"
    }
@app.post("/signup")
def signup(data: SignupRequest):
    response = supabase.auth.sign_up({
        "email": data.email,
        "password": data.password
    })

    return {
        "message": "Signup successful",
        "user": response.user
    }
@app.get("/")
def root():
    return {
        "name": "Task API Auth",
        "status": "ok"
    }

@app.get("/protected")
def protected_route(user=Depends(verify_token)):
    return {
        "message": "You have access to this protected route",
        "user_id": user.id,
        "email": user.email
    }