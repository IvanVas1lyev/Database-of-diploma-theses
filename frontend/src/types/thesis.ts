export interface Student {
  id: string; // Changed from number to string (format: year_directory)
  name: string;
  email: string;
  graduation_year: number;
  thesis: {
    title: string;
    summary: string;
    advisor: string;
    keywords: string[];
    defense_date: string;
  };
  code: {
    has_code: boolean;
    main_file: string | null;
    description: string | null;
    files?: string[];
  };
  student_dir: string;
  added_date: string;
  
  // Legacy fields for compatibility
  thesis_title?: string;
  thesis_summary?: string;
  python_code?: string;
  created_at?: string;
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
  student_id: string; // Changed from number to string
  input_args?: string;
  output_result?: string;
  success: boolean;
  error_message?: string;
  executed_at: string;
}

export interface CodeInfo {
  has_code: boolean;
  main_file?: string;
  description?: string;
  files: Array<{
    name: string;
    size: number;
    is_main: boolean;
  }>;
}

export interface Statistics {
  total_students: number;
  total_years: number;
  students_with_code: number;
  years_range: {
    min: number | null;
    max: number | null;
  };
  by_year: Record<number, {
    count: number;
    with_code: number;
  }>;
}