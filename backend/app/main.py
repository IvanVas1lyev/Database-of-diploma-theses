from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine
from .models import thesis
from .api.endpoints import students, execute

# Create database tables
thesis.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.project_name,
    openapi_url=f"{settings.api_v1_str}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    students.router,
    prefix=f"{settings.api_v1_str}/students",
    tags=["students"]
)

app.include_router(
    execute.router,
    prefix=f"{settings.api_v1_str}/students",
    tags=["execution"]
)


@app.get("/")
def read_root():
    return {"message": "Thesis Database API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}