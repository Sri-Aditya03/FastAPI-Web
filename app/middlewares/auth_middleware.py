from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse

from app.middlewares.jwt_core import decode_jwt


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        path = request.url.path

        # Public paths
        public_paths = [
            "/", "/auth/login", "/auth/signup"
        ]

        if path.startswith("/static"):
            return await call_next(request)

        if path in public_paths:
            return await call_next(request)

        if path.startswith("/dashboard"):
            token = request.cookies.get("access_token")

            if not token:
                return RedirectResponse("/", status_code=303)

            email = decode_jwt(token)

            if not email:
                return RedirectResponse("/", status_code=303)

            request.state.user = email

        return await call_next(request)
