from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.helpers.auth_helpers import (
    create_user_helper,
    authenticate_user_helper,
    check_user_exists_helper
)
from app.middlewares.jwt_core import create_jwt


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ------------------------
# SIGNUP PAGE
# ------------------------
@router.get("/auth/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})


# ------------------------
# SIGNUP SUBMIT
# ------------------------
@router.post("/auth/signup")
def signup(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):

    if password != confirm_password:
        return templates.TemplateResponse(
            "auth/signup.html",
            {"request": {}, "error": "Passwords do not match"}
        )

    if check_user_exists_helper(email, phone):
        return templates.TemplateResponse(
            "auth/signup.html",
            {"request": {}, "error": "User already exists"}
        )

    create_user_helper(name, email, phone, password)

    token = create_jwt(email)

    res = RedirectResponse("/dashboard", status_code=303)
    res.set_cookie("access_token", token, httponly=True)

    return res


# ------------------------
# LOGIN SUBMIT
# ------------------------
@router.post("/auth/login")
def login(
    email: str = Form(...),
    password: str = Form(...)
):

    user = authenticate_user_helper(email, password)

    if not user:
        return RedirectResponse("/auth/signup", status_code=303)

    token = create_jwt(email)
    res = RedirectResponse("/dashboard", status_code=303)
    res.set_cookie("access_token", token, httponly=True)

    return res


@router.get("/auth/logout")
def logout():
    res = RedirectResponse("/", status_code=303)
    res.delete_cookie("access_token")
    return res
