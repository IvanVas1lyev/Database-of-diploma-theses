from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...schemas.thesis import ExecutionRequest, ExecutionResult, ExecutionLog
from ...services.student_service import StudentService
from ...services.executor import executor
from typing import List

router = APIRouter()


@router.post("/{student_id}/execute", response_model=ExecutionResult)
def execute_student_code(
    student_id: int,
    request: ExecutionRequest,
    db: Session = Depends(get_db)
):
    """Execute student's Python code with provided arguments"""
    # Get student
    student = StudentService.get_student(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if not student.python_code:
        raise HTTPException(status_code=400, detail="Student has no Python code to execute")
    
    # Execute code
    success, result, error, execution_time = executor.execute_code(
        code=student.python_code,
        args=request.args
    )
    
    # Log execution
    StudentService.log_execution(
        db=db,
        student_id=student_id,
        input_args=request.args,
        output_result=result if success else None,
        success=success,
        error_message=error
    )
    
    return ExecutionResult(
        success=success,
        result=result,
        error=error,
        execution_time=execution_time
    )


@router.get("/{student_id}/logs", response_model=List[ExecutionLog])
def get_execution_logs(
    student_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent execution logs for a student"""
    # Verify student exists
    student = StudentService.get_student(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return StudentService.get_execution_logs(db=db, student_id=student_id, limit=limit)