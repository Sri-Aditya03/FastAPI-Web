# FastAPI Authentication Project

A complete authentication system using:
- FastAPI
- Elasticsearch
- Kibana
- Jinja2 Templates
- JWT Authentication
- Login, Signup, Dashboard

## Run the project

### Start Elasticsearch & Kibana
docker compose up -d

### Start FastAPI
uvicorn app.main:app --reload 
