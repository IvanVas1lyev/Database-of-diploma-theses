# Thesis Database Web Application

A comprehensive web application for storing, searching, and managing graduation theses of statistics department students. Built with modern technologies and designed for easy deployment and maintenance.

## 🚀 Features

### Core Functionality
- **Advanced Search**: Full-text search across thesis titles, summaries, and student names
- **Year-based Organization**: Browse theses by graduation year
- **Student Profiles**: Detailed pages for each student with thesis information
- **Interactive Code Execution**: Safe Python code execution with custom functions
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### Technical Features
- **RESTful API**: Well-documented FastAPI backend with automatic OpenAPI documentation
- **Modern Frontend**: React with TypeScript for type safety and better development experience
- **Database Integration**: PostgreSQL with full-text search capabilities
- **Containerized Deployment**: Docker and Docker Compose for easy setup
- **Sample Data**: Pre-populated with realistic thesis examples

## 🛠 Technology Stack

- **Backend**: FastAPI (Python) with SQLAlchemy ORM
- **Frontend**: React 18 with TypeScript and Tailwind CSS
- **Database**: PostgreSQL 15
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (production)

## 📋 Prerequisites

- Docker and Docker Compose installed
- Git for cloning the repository
- (Optional) Node.js 18+ and Python 3.11+ for local development

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended if available)

1. **Install Docker Compose** (if not already installed):
   ```bash
   # On macOS with Homebrew
   brew install docker-compose
   
   # On Ubuntu/Debian
   sudo apt-get install docker-compose
   
   # Or use Docker Desktop which includes Compose
   ```

2. **Clone and start**:
   ```bash
   git clone <repository-url>
   cd thesis-database
   docker-compose up --build
   ```

### Option 2: Using Docker Compose V2 (Modern Docker)

If you have modern Docker installed, use:
```bash
cd thesis-database
docker compose up --build
```

### Option 3: Manual Setup (No Docker required)

#### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 12+

#### 1. Database Setup
```bash
# Install and start PostgreSQL
brew install postgresql  # macOS
# or
sudo apt-get install postgresql postgresql-contrib  # Ubuntu

# Create database
createdb thesis_db
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env to set DATABASE_URL=postgresql://postgres:password@localhost:5432/thesis_db

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Setup (in new terminal)
```bash
cd frontend
npm install
npm start
```

#### 4. Create Sample Data (in new terminal)
```bash
cd backend
source venv/bin/activate
python -c "from app.utils.sample_data import create_sample_data; create_sample_data()"
```

### Option 4: Individual Docker Containers

If you have Docker but not Docker Compose:

#### 1. Start PostgreSQL
```bash
docker run --name thesis_db -e POSTGRES_DB=thesis_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15-alpine
```

#### 2. Build and run backend
```bash
cd backend
docker build -t thesis-backend .
docker run --name thesis_backend -p 8000:8000 --link thesis_db:db -e DATABASE_URL=postgresql://postgres:password@db:5432/thesis_db -d thesis-backend
```

#### 3. Build and run frontend
```bash
cd frontend
docker build -t thesis-frontend .
docker run --name thesis_frontend -p 3000:80 -d thesis-frontend
```

## 🌐 Access Points

Once running (any method):
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432 (postgres/password)

## 📁 Project Structure

```
thesis-database/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Configuration and database
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── utils/             # Utilities and sample data
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API client
│   │   └── types/             # TypeScript definitions
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml          # Full stack orchestration
├── .env.example               # Environment variables template
└── README.md
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/thesis_db

# API Settings
CODE_EXECUTION_TIMEOUT=5
MAX_CODE_LENGTH=1000

# Frontend
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 📖 API Documentation

The backend provides comprehensive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `GET /api/v1/students/search` - Search students and theses
- `GET /api/v1/students/{id}` - Get student details
- `POST /api/v1/students/{id}/execute` - Execute Python code
- `GET /api/v1/students/years` - Get graduation years

## 🧪 Sample Data

The application includes sample data with 6 realistic thesis examples:

- **Alice Johnson (2024)**: Machine Learning in Financial Risk Assessment
- **Bob Chen (2024)**: Bayesian Analysis of Climate Change Data
- **Carol Davis (2023)**: Statistical Methods for Social Media Sentiment Analysis
- **David Wilson (2023)**: Time Series Analysis of Economic Indicators
- **Emma Thompson (2022)**: Statistical Quality Control in Manufacturing
- **Frank Rodriguez (2022)**: Survival Analysis in Medical Statistics

Each student has interactive Python code demonstrating statistical concepts.

## 🔒 Security Features

- **Safe Code Execution**: Restricted Python environment with limited imports
- **Input Validation**: Comprehensive validation on all API endpoints
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **CORS Configuration**: Properly configured cross-origin requests
- **Timeout Protection**: Code execution timeout limits

## 🚀 Deployment

### Production Deployment

1. **Configure environment variables** for production
2. **Build and deploy** using Docker Compose:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Scaling Considerations

- Use a reverse proxy (nginx) for load balancing
- Configure PostgreSQL for production workloads
- Implement Redis for caching (future enhancement)
- Set up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 Adding New Students

Students can be added via:

1. **API**: POST to `/api/v1/students/`
2. **Database**: Direct insertion into the students table
3. **Sample Data Script**: Modify `backend/app/utils/sample_data.py`

### Student Data Format

```json
{
  "name": "Student Name",
  "graduation_year": 2024,
  "thesis_title": "Thesis Title",
  "thesis_summary": "Detailed summary...",
  "python_code": "# Optional Python code\nprint('Hello, World!')"
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection**: Ensure PostgreSQL is running and accessible
2. **Port Conflicts**: Check if ports 3000, 8000, or 5432 are in use
3. **Docker Issues**: Try `docker-compose down` and rebuild
4. **Code Execution**: Check Python code syntax and allowed imports

### Logs

View application logs:
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent Python web framework
- React team for the robust frontend library
- PostgreSQL for reliable database functionality
- Docker for containerization capabilities