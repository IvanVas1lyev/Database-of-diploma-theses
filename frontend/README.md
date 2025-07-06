# Thesis Database Frontend

React TypeScript frontend for the thesis database application.

## Features

- Modern React with TypeScript
- Responsive design with Tailwind CSS
- Search and browse functionality
- Interactive Python code execution
- Student and thesis management interface

## Pages

- **Home Page** - Search interface and recent additions
- **Student Page** - Individual student details with code execution
- **Year Page** - Students grouped by graduation year

## Components

- **SearchBar** - Advanced search with filters
- **StudentCard** - Student information display
- **CodeExecutor** - Interactive Python code runner

## Development Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp ../.env.example .env.local
   ```

3. Start development server:
   ```bash
   npm start
   ```

4. Build for production:
   ```bash
   npm run build
   ```

## Docker

Build and run with Docker:
```bash
docker build -t thesis-frontend .
docker run -p 3000:80 thesis-frontend
```

## Technologies Used

- React 18
- TypeScript
- React Router
- Axios for API calls
- Tailwind CSS for styling
- Nginx for production serving

## Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:8000/api/v1)