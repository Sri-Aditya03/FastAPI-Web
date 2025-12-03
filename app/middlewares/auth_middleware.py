from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse
from jose import JWTError
from app.core.jwt_handler import decode_access_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        protected_paths = ["/dashboard"]

        if any(request.url.path.startswith(path) for path in protected_paths):
            token = request.cookies.get("access_token")

            if not token:
                return RedirectResponse("/")

            try:
                decode_access_token(token)
            except JWTError:
                return RedirectResponse("/")

        response = await call_next(request)
        return response
