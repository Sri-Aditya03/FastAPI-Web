from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.services.user_service import create_user, authenticate_user
from app.services.elastic_service import get_user_by_email
from app.core.jwt_handler import create_access_token

router = APIRouter()

# Template Engine
templates = Jinja2Templates(directory="app/templates")


# ============================================================
# LOGIN PAGE  →  "/"
# ============================================================
@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


# ============================================================
# LOGIN POST → "/auth/login"
# ============================================================
@router.post("/auth/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email)

    # If no user found → redirect signup
    if not user:
        return RedirectResponse("/auth/signup", status_code=303)

    # Check password
    authenticated = authenticate_user(email, password)

    if not authenticated:
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": {},
                "error": "Incorrect password"
            }
        )

    # Valid user → create JWT cookie
    token = create_access_token(email)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("access_token", token, httponly=True)

    return response


# ============================================================
# SIGNUP PAGE  →  "/auth/signup"
# ============================================================
@router.get("/auth/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})


# ============================================================
# SIGNUP POST → "/auth/signup"
# Stores user in Elasticsearch → redirects dashboard
# ============================================================
@router.post("/auth/signup")
def signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    # Check password match
    if password != confirm_password:
        return templates.TemplateResponse(
            "auth/signup.html",
            {
                "request": {},
                "error": "Passwords do not match"
            }
        )

    # Create user in Elasticsearch
    create_user(name, email, password)

    # Create login session
    token = create_access_token(email)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("access_token", token, httponly=True)

    return response


# ============================================================
# LOGOUT → "/auth/logout"
# ============================================================
@router.get("/auth/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response
