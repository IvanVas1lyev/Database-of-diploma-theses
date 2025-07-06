from fastapi import APIRouter, HTTPException
from ...schemas.thesis import ExecutionRequest, ExecutionResult
from ...services.file_service import FileStudentService
from ...services.executor import executor

router = APIRouter()
file_service = FileStudentService()


@router.post("/{student_id}/execute", response_model=ExecutionResult)
def execute_student_code(
    student_id: str,
    request: ExecutionRequest
):
    """Execute student's Python code with provided arguments"""
    # Get student
    student = file_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    
    # Check if student has code
    code_info = student.get('code', {})
    if not code_info.get('has_code', False):
        raise HTTPException(status_code=400, detail="У студента нет кода для выполнения")
    
    main_file = code_info.get('main_file')
    if not main_file:
        raise HTTPException(status_code=400, detail="Не указан основной файл кода")
    
    # Get code content
    code_content = file_service.get_student_code_file(student_id, main_file)
    if not code_content:
        raise HTTPException(status_code=404, detail="Файл кода не найден")
    
    # Execute code
    success, result, error, execution_time = executor.execute_code(
        code=code_content,
        args=request.args
    )
    
    return ExecutionResult(
        success=success,
        result=result,
        error=error,
        execution_time=execution_time
    )


@router.get("/{student_id}/code")
def get_student_code_info(student_id: str):
    """Get information about student's code files"""
    student = file_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    
    code_info = student.get('code', {})
    if not code_info.get('has_code', False):
        return {"has_code": False, "files": []}
    
    # Get list of code files
    try:
        year_str, student_dir = student_id.split('_', 1)
        year = int(year_str)
        code_path = file_service.data_path / str(year) / student_dir / "code"
        
        files = []
        if code_path.exists():
            for file_path in code_path.iterdir():
                if file_path.is_file():
                    files.append({
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "is_main": file_path.name == code_info.get('main_file')
                    })
        
        return {
            "has_code": True,
            "main_file": code_info.get('main_file'),
            "description": code_info.get('description'),
            "files": files
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения информации о коде: {str(e)}")


@router.get("/{student_id}/code/{filename}")
def get_student_code_file(student_id: str, filename: str):
    """Get content of a specific code file"""
    student = file_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    
    code_info = student.get('code', {})
    if not code_info.get('has_code', False):
        raise HTTPException(status_code=400, detail="У студента нет кода")
    
    # Get code file content
    content = file_service.get_student_code_file(student_id, filename)
    if content is None:
        raise HTTPException(status_code=404, detail="Файл кода не найден")
    
    return {"content": content, "filename": filename}