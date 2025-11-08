from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

router = APIRouter(prefix="/auth", tags=["Auth"])

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")
ALGORITHM = "HS256"

# Dummy user database
users_db = {
    "analyst": {"username": "analyst", "password": "analyst123", "role": "analyst"},
    "cro": {"username": "cro", "password": "cro123", "role": "cro"}
}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"sub": user["username"], "role": user["role"], "exp": datetime.utcnow() + timedelta(hours=3)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}
