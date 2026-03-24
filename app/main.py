from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from service.routes import api_v1_router

app = FastAPI(title="Taskmaster API", version="1.0.0")

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(api_v1_router)
