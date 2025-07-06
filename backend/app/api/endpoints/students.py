from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...schemas.thesis import Student, StudentCreate, StudentUpdate, SearchResponse
from ...services.student_service import StudentService
import math

router = APIRouter()


@router.post("/", response_model=Student)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    """Create a new student"""
    return StudentService.create_student(db=db, student=student)


@router.get("/", response_model=List[Student])
def read_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all students with pagination"""
    return StudentService.get_students(db=db, skip=skip, limit=limit)


@router.get("/search", response_model=SearchResponse)
def search_students(
    q: Optional[str] = Query(None, description="Search query for name, title, or summary"),
    year: Optional[int] = Query(None, description="Filter by graduation year"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search students by query and/or year"""
    students, total = StudentService.search_students(
        db=db, query=q, year=year, page=page, per_page=per_page
    )
    
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    
    return SearchResponse(
        students=students,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@router.get("/years", response_model=List[int])
def get_graduation_years(db: Session = Depends(get_db)):
    """Get all unique graduation years"""
    return StudentService.get_graduation_years(db=db)


@router.get("/years/{year}", response_model=List[Student])
def get_students_by_year(
    year: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get students by graduation year"""
    return StudentService.get_students_by_year(db=db, year=year, skip=skip, limit=limit)


@router.get("/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """Get student by ID"""
    student = StudentService.get_student(db=db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=Student)
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    """Update student information"""
    student = StudentService.update_student(db=db, student_id=student_id, student_update=student_update)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete student"""
    success = StudentService.delete_student(db=db, student_id=student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}