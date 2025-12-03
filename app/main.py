from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import auth_router, dashboard_router
from app.middlewares.auth_middleware import AuthMiddleware
from app.services.elastic_service import init_index

app = FastAPI()

init_index()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(AuthMiddleware)

app.include_router(auth_router.router)
app.include_router(dashboard_router.router)

@app.get("/health")
def health():
    return {"status": "OK"}
