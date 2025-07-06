from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.endpoints import students, execute

app = FastAPI(
    title=settings.project_name,
    description="База данных дипломных работ кафедры математической статистики и случайных процессов МГУ",
    version="2.0.0",
    openapi_url=f"{settings.api_v1_str}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Убираем PUT, DELETE - только чтение и выполнение кода
    allow_headers=["*"],
)

# Include routers
app.include_router(
    students.router,
    prefix=f"{settings.api_v1_str}",
    tags=["students"]
)

app.include_router(
    execute.router,
    prefix=f"{settings.api_v1_str}/students",
    tags=["execution"]
)


@app.get("/")
def read_root():
    return {
        "message": "База данных дипломных работ МГУ", 
        "version": "2.0.0",
        "description": "Кафедра математической статистики и случайных процессов",
        "data_source": "file_system"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "storage": "file_system"}