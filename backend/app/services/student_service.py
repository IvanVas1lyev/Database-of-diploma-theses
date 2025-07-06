from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from ..models.thesis import Student, ExecutionLog
from ..schemas.thesis import StudentCreate, StudentUpdate
import math


class StudentService:
    """Service class for student-related operations"""
    
    @staticmethod
    def create_student(db: Session, student: StudentCreate) -> Student:
        """Create a new student"""
        db_student = Student(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    
    @staticmethod
    def get_student(db: Session, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        return db.query(Student).filter(Student.id == student_id).first()
    
    @staticmethod
    def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
        """Get all students with pagination"""
        return db.query(Student).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_students_by_year(db: Session, year: int, skip: int = 0, limit: int = 100) -> List[Student]:
        """Get students by graduation year"""
        return db.query(Student).filter(Student.graduation_year == year).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_student(db: Session, student_id: int, student_update: StudentUpdate) -> Optional[Student]:
        """Update student information"""
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            return None
        
        update_data = student_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_student, field, value)
        
        db.commit()
        db.refresh(db_student)
        return db_student
    
    @staticmethod
    def delete_student(db: Session, student_id: int) -> bool:
        """Delete student"""
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            return False
        
        db.delete(db_student)
        db.commit()
        return True
    
    @staticmethod
    def search_students(
        db: Session, 
        query: Optional[str] = None,
        year: Optional[int] = None,
        page: int = 1,
        per_page: int = 20
    ) -> tuple[List[Student], int]:
        """
        Search students by query and/or year
        Returns tuple of (students, total_count)
        """
        db_query = db.query(Student)
        
        # Apply filters
        filters = []
        
        if query:
            # Search in name, thesis_title, and thesis_summary
            search_filter = or_(
                Student.name.ilike(f"%{query}%"),
                Student.thesis_title.ilike(f"%{query}%"),
                Student.thesis_summary.ilike(f"%{query}%")
            )
            filters.append(search_filter)
        
        if year:
            filters.append(Student.graduation_year == year)
        
        if filters:
            db_query = db_query.filter(and_(*filters))
        
        # Get total count
        total = db_query.count()
        
        # Apply pagination
        skip = (page - 1) * per_page
        students = db_query.offset(skip).limit(per_page).all()
        
        return students, total
    
    @staticmethod
    def get_graduation_years(db: Session) -> List[int]:
        """Get all unique graduation years"""
        years = db.query(Student.graduation_year).distinct().order_by(Student.graduation_year.desc()).all()
        return [year[0] for year in years]
    
    @staticmethod
    def log_execution(
        db: Session,
        student_id: int,
        input_args: Optional[str],
        output_result: Optional[str],
        success: bool,
        error_message: Optional[str] = None
    ) -> ExecutionLog:
        """Log code execution result"""
        log_entry = ExecutionLog(
            student_id=student_id,
            input_args=input_args,
            output_result=output_result,
            success=success,
            error_message=error_message
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry
    
    @staticmethod
    def get_execution_logs(db: Session, student_id: int, limit: int = 10) -> List[ExecutionLog]:
        """Get recent execution logs for a student"""
        return db.query(ExecutionLog).filter(
            ExecutionLog.student_id == student_id
        ).order_by(ExecutionLog.executed_at.desc()).limit(limit).all()