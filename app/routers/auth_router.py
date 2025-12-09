from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from app.helpers.auth_helpers import (
    validate_signup_fields,
    create_user_helper,
    validate_login
)
from app.middlewares.jwt_core import create_jwt
from app.services.redis_service import store_token, blacklist_token

router = APIRouter(prefix="/auth")


# -----------------------------------
# GET: SIGNUP PAGE
# -----------------------------------
@router.get("/signup")
def signup_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "auth/signup.html",
        {"request": request}
    )


# -----------------------------------
# POST: SIGNUP SUBMIT
# -----------------------------------
@router.post("/signup")
def signup(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):

    error = validate_signup_fields(name, email, phone, password, confirm_password)
    if error:
        return request.app.state.templates.TemplateResponse(
            "auth/signup.html",
            {"request": request, "error": error}
        )

    # Creates user (with MD5 user_id but RAW password)
    create_user_helper(name, email, phone, password)

    return RedirectResponse(url="/auth/login", status_code=303)


# -----------------------------------
# GET: LOGIN PAGE
# -----------------------------------
@router.get("/login")
def login_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "auth/login.html",
        {"request": request}
    )


# -----------------------------------
# POST: LOGIN SUBMIT
# -----------------------------------
@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = validate_login(email, password)

    if not user:
        return request.app.state.templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    # LOGIN SUCCESS → CREATE JWT, STORE IN REDIS, AND SET COOKIE
    token = create_jwt(user["email"])
    store_token(user["user_id"], token)
    
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie("access_token", token, httponly=True)
    return response


# -----------------------------------
# LOGOUT
# -----------------------------------
@router.get("/logout")
def logout(request: Request):
    token = request.cookies.get("access_token")
    
    # Blacklist the token in Redis
    if token:
        blacklist_token(token)
    
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response
