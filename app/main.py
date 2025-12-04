from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.index import router as index_router
from app.routers.auth_router import router as auth_router
from app.routers.dashboard_router import router as dashboard_router

from app.middlewares.auth_middleware import AuthMiddleware
from app.services.elastic_service import init_index


app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Middlewares
app.add_middleware(AuthMiddleware)

# Routers
app.include_router(index_router)
app.include_router(auth_router)
app.include_router(dashboard_router)

# Initialize ES
@app.on_event("startup")
def startup_event():
    init_index()
