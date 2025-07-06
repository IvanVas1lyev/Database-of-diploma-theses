import axios from 'axios';
import { Student, SearchResponse, ExecutionRequest, ExecutionResult } from '../types/thesis';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const studentApi = {
  // Get all students
  getStudents: async (): Promise<Student[]> => {
    const response = await api.get('/students');
    return response.data.students;
  },

  // Get student by ID (now string format: year_directory)
  getStudent: async (id: string): Promise<Student> => {
    const response = await api.get(`/students/${id}`);
    return response.data;
  },

  // Search students
  searchStudents: async (
    query?: string,
    year?: number
  ): Promise<SearchResponse> => {
    const params = new URLSearchParams();
    if (query) params.append('search', query);
    if (year) params.append('year', year.toString());

    const response = await api.get(`/students?${params}`);
    return {
      students: response.data.students,
      total: response.data.total,
      page: 1,
      per_page: response.data.total,
      total_pages: 1
    };
  },

  // Get graduation years
  getGraduationYears: async (): Promise<number[]> => {
    const response = await api.get('/years');
    return response.data.years;
  },

  // Get students by year
  getStudentsByYear: async (year: number): Promise<Student[]> => {
    const response = await api.get(`/students?year=${year}`);
    return response.data.students;
  },

  // Execute student code
  executeCode: async (studentId: string, request: ExecutionRequest): Promise<ExecutionResult> => {
    const response = await api.post(`/students/${studentId}/execute`, request);
    return response.data;
  },

  // Get student code info
  getStudentCodeInfo: async (studentId: string) => {
    const response = await api.get(`/students/${studentId}/code`);
    return response.data;
  },

  // Get student code file
  getStudentCodeFile: async (studentId: string, filename: string) => {
    const response = await api.get(`/students/${studentId}/code/${filename}`);
    return response.data;
  },

  // Get statistics
  getStatistics: async () => {
    const response = await api.get('/statistics');
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  }
};

export default api;