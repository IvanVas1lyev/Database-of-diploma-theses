export interface Student {
  id: number;
  name: string;
  graduation_year: number;
  thesis_title: string;
  thesis_summary: string;
  python_code?: string;
  created_at: string;
  updated_at?: string;
}

export interface SearchResponse {
  students: Student[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface ExecutionRequest {
  args?: string;
}

export interface ExecutionResult {
  success: boolean;
  result?: string;
  error?: string;
  execution_time?: number;
}

export interface ExecutionLog {
  id: number;
  student_id: number;
  input_args?: string;
  output_result?: string;
  success: boolean;
  error_message?: string;
  executed_at: string;
}