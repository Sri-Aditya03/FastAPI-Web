from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.middlewares.jwt_core import decode_jwt
from app.services.redis_service import is_token_blacklisted

router = APIRouter()

@router.get("/dashboard")
def dashboard(request: Request):

    token = request.cookies.get("access_token")

    # No token, invalid token, or blacklisted token → redirect to login
    if not token or not decode_jwt(token) or is_token_blacklisted(token):
        return RedirectResponse("/auth/login", status_code=303)

    return request.app.state.templates.TemplateResponse(
        "dashboard/dashboard.html",
        {"request": request}
    )
