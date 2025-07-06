from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    graduation_year: int = Field(..., ge=1900, le=2100)
    thesis_title: str = Field(..., min_length=1, max_length=500)
    thesis_summary: str = Field(..., min_length=1)
    python_code: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    graduation_year: Optional[int] = Field(None, ge=1900, le=2100)
    thesis_title: Optional[str] = Field(None, min_length=1, max_length=500)
    thesis_summary: Optional[str] = Field(None, min_length=1)
    python_code: Optional[str] = None


class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExecutionRequest(BaseModel):
    args: Optional[str] = None


class ExecutionResult(BaseModel):
    success: bool
    result: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None


class ExecutionLogBase(BaseModel):
    student_id: int
    input_args: Optional[str] = None
    output_result: Optional[str] = None
    success: bool = False
    error_message: Optional[str] = None


class ExecutionLog(ExecutionLogBase):
    id: int
    executed_at: datetime

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    students: list[Student]
    total: int
    page: int
    per_page: int
    total_pages: int