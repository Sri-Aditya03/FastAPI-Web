from datetime import datetime, timedelta
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM

def create_access_token(email: str):
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
