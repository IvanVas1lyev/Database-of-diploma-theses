# Thesis Database Backend

FastAPI backend for the thesis database application.

## Features

- RESTful API for thesis and student management
- Full-text search capabilities
- Safe Python code execution
- PostgreSQL database integration
- Automatic API documentation with Swagger/OpenAPI

## API Endpoints

### Students
- `GET /api/v1/students/` - List all students
- `GET /api/v1/students/{id}` - Get student by ID
- `GET /api/v1/students/search` - Search students
- `GET /api/v1/students/years` - Get graduation years
- `GET /api/v1/students/years/{year}` - Get students by year
- `POST /api/v1/students/` - Create new student
- `PUT /api/v1/students/{id}` - Update student
- `DELETE /api/v1/students/{id}` - Delete student

### Code Execution
- `POST /api/v1/students/{id}/execute` - Execute student's Python code
- `GET /api/v1/students/{id}/logs` - Get execution logs

## Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp ../.env.example .env
   ```

3. Start PostgreSQL database (or use Docker Compose)

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Create sample data:
   ```bash
   python -c "from app.utils.sample_data import create_sample_data; create_sample_data()"
   ```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker

Build and run with Docker:
```bash
docker build -t thesis-backend .
docker run -p 8000:8000 thesis-backend
```

## Testing

Run tests:
```bash
pytest