import jwt
from datetime import datetime, timedelta

SECRET = "MY_SECRET"
ALGO = "HS256"

def create_jwt(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=5)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_jwt(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        return data["sub"]
    except:
        return None
