from app.core.security import hash_password, verify_password
from app.services.elastic_service import insert_user, get_user_by_email

def create_user(name: str, email: str, password: str):
    password = password.strip()[:72]  # fix bcrypt limit
    hashed = hash_password(password)

    user = {
        "name": name,
        "email": email,
        "password": hashed
    }

    insert_user(user)
    return user


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    return user  # return userdata for dashboard use
