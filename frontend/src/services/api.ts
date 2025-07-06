import axios from 'axios';
import { Student, SearchResponse, ExecutionRequest, ExecutionResult, ExecutionLog } from '../types/thesis';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const studentApi = {
  // Get all students
  getStudents: async (skip = 0, limit = 100): Promise<Student[]> => {
    const response = await api.get(`/students/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // Get student by ID
  getStudent: async (id: number): Promise<Student> => {
    const response = await api.get(`/students/${id}`);
    return response.data;
  },

  // Search students
  searchStudents: async (
    query?: string,
    year?: number,
    page = 1,
    perPage = 20
  ): Promise<SearchResponse> => {
    const params = new URLSearchParams();
    if (query) params.append('q', query);
    if (year) params.append('year', year.toString());
    params.append('page', page.toString());
    params.append('per_page', perPage.toString());

    const response = await api.get(`/students/search?${params}`);
    return response.data;
  },

  // Get graduation years
  getGraduationYears: async (): Promise<number[]> => {
    const response = await api.get('/students/years');
    return response.data;
  },

  // Get students by year
  getStudentsByYear: async (year: number, skip = 0, limit = 100): Promise<Student[]> => {
    const response = await api.get(`/students/years/${year}?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // Execute student code
  executeCode: async (studentId: number, request: ExecutionRequest): Promise<ExecutionResult> => {
    const response = await api.post(`/students/${studentId}/execute`, request);
    return response.data;
  },

  // Get execution logs
  getExecutionLogs: async (studentId: number, limit = 10): Promise<ExecutionLog[]> => {
    const response = await api.get(`/students/${studentId}/logs?limit=${limit}`);
    return response.data;
  },
};

export default api;