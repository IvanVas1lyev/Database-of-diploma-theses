"""
API endpoints для работы со студентами (файловая система)
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.services.file_service import FileStudentService

router = APIRouter()
file_service = FileStudentService()

@router.get("/students")
async def get_students(
    year: Optional[int] = Query(None, description="Фильтр по году выпуска"),
    search: Optional[str] = Query(None, description="Поисковый запрос")
):
    """
    Получение списка студентов с возможностью фильтрации и поиска
    """
    try:
        if search:
            students = file_service.search_students(search)
        elif year:
            students = file_service.get_students_by_year(year)
        else:
            students = file_service.get_all_students()
        
        return {
            "students": students,
            "total": len(students)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных: {str(e)}")

@router.get("/students/{student_id}")
async def get_student(student_id: str):
    """
    Получение информации о конкретном студенте
    """
    student = file_service.get_student_by_id(student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    
    return student

@router.get("/students/{student_id}/code/{filename}")
async def get_student_code_file(student_id: str, filename: str):
    """
    Получение файла кода студента
    """
    content = file_service.get_student_code_file(student_id, filename)
    
    if content is None:
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    return {
        "filename": filename,
        "content": content
    }

@router.get("/years")
async def get_available_years():
    """
    Получение списка доступных годов выпуска
    """
    years = file_service.get_available_years()
    return {"years": years}

@router.get("/statistics")
async def get_statistics():
    """
    Получение статистики по базе данных
    """
    stats = file_service.get_statistics()
    return stats

@router.get("/health")
async def health_check():
    """
    Проверка работоспособности API
    """
    try:
        # Проверяем доступность файловой системы
        stats = file_service.get_statistics()
        return {
            "status": "healthy",
            "data_available": stats["total_students"] > 0,
            "total_students": stats["total_students"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Сервис недоступен: {str(e)}")