from app.hashing.md5_hash import md5_hash
from app.services.elastic_service import (
    insert_user_es,
    get_user_by_email_phone_es
)


def generate_user_id(email: str, phone: str) -> str:
    return md5_hash(email + phone)


def create_user_helper(name, email, phone, password):
    hashed_pw = md5_hash(password)

    user_id = generate_user_id(email, phone)

    user_doc = {
        "id": user_id,
        "name": name,
        "email": email,
        "phone": phone,
        "password": hashed_pw
    }

    insert_user_es(user_id, user_doc)


def check_user_exists_helper(email, phone):
    return get_user_by_email_phone_es(email, phone)


def authenticate_user_helper(email: str, password: str):
    user = get_user_by_email_phone_es(email)

    if not user:
        return None

    hashed = md5_hash(password)

    if user["password"] != hashed:
        return None

    return user
