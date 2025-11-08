import fastapi
import fastapi.security
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
from jose import jwt, JWTError

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = fastapi.Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload.get("sub"), "role": payload.get("role")}
    except JWTError:
        raise fastapi.HTTPException(status_code=401, detail="Invalid token")

def check_access(user, allowed_roles):
    if user["role"] not in allowed_roles:
        raise fastapi.HTTPException(status_code=403, detail="Access denied")
