from datetime import datetime
from app.hashing.md5_hash import md5_hash
from app.services.elastic_service import (
    insert_user_es,
    get_user_by_email_es   # UPDATED
)


def validate_signup_fields(name: str, email: str, phone: str, password: str, confirm_password: str):
    if password != confirm_password:
        return "Passwords do not match."
    if not name or not email or not phone or not password:
        return "All fields are required."
    return None


def create_user_helper(name: str, email: str, phone: str, password: str):

    # Generate hashed user_id
    user_id = md5_hash(email + phone)

    # User document stored in Elasticsearch
    user_data = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "phone": phone,
        "password": password,  
        "created_at": datetime.utcnow().isoformat()
    }

    insert_user_es(user_id, user_data)

    return user_data


def validate_login(email: str, password: str):
 

    # Fetch user based ONLY on email
    user = get_user_by_email_es(email)

    if not user:
        return None

    stored_password = user["_source"]["password"]

    # Compare raw password
    if stored_password != password:
        return None

    return user["_source"]
