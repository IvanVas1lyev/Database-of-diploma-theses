"""
Сервис для работы с файловой системой данных студентов
"""

import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

class FileStudentService:
    """
    Сервис для работы с данными студентов, хранящимися в файловой системе
    """
    
    def __init__(self, data_path: str = "data"):
        self.data_path = Path(data_path)
        if not self.data_path.exists():
            self.data_path.mkdir(parents=True, exist_ok=True)
    
    def _load_student_info(self, year: int, student_dir: str) -> Optional[Dict[str, Any]]:
        """
        Загрузка информации о студенте из файла info.json
        """
        info_path = self.data_path / str(year) / student_dir / "info.json"
        
        if not info_path.exists():
            return None
        
        try:
            with open(info_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Добавляем дополнительную информацию
            data['id'] = f"{year}_{student_dir}"
            data['student_dir'] = student_dir
            data['added_date'] = datetime.fromtimestamp(info_path.stat().st_mtime).isoformat()
            
            # Проверяем наличие кода
            code_path = self.data_path / str(year) / student_dir / "code"
            if code_path.exists() and data.get('code', {}).get('has_code', False):
                data['code']['files'] = [f.name for f in code_path.iterdir() if f.is_file()]
            
            return data
            
        except (json.JSONDecodeError, KeyError, OSError) as e:
            print(f"Ошибка загрузки данных студента {student_dir} ({year}): {e}")
            return None
    
    def get_all_students(self) -> List[Dict[str, Any]]:
        """
        Получение всех студентов из всех годов
        """
        students = []
        
        # Проходим по всем годам
        for year_dir in self.data_path.iterdir():
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue
                
            year = int(year_dir.name)
            
            # Проходим по всем студентам в году
            for student_dir in year_dir.iterdir():
                if not student_dir.is_dir():
                    continue
                    
                student_info = self._load_student_info(year, student_dir.name)
                if student_info:
                    students.append(student_info)
        
        # Сортируем по году выпуска и имени
        students.sort(key=lambda x: (x['graduation_year'], x['name']))
        return students
    
    def get_students_by_year(self, year: int) -> List[Dict[str, Any]]:
        """
        Получение студентов определенного года
        """
        students = []
        year_path = self.data_path / str(year)
        
        if not year_path.exists():
            return students
        
        for student_dir in year_path.iterdir():
            if not student_dir.is_dir():
                continue
                
            student_info = self._load_student_info(year, student_dir.name)
            if student_info:
                students.append(student_info)
        
        # Сортируем по имени
        students.sort(key=lambda x: x['name'])
        return students
    
    def get_student_by_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        Получение студента по ID (формат: год_директория)
        """
        try:
            year_str, student_dir = student_id.split('_', 1)
            year = int(year_str)
            return self._load_student_info(year, student_dir)
        except (ValueError, IndexError):
            return None
    
    def search_students(self, query: str) -> List[Dict[str, Any]]:
        """
        Поиск студентов по запросу
        """
        if not query:
            return self.get_all_students()
        
        query_lower = query.lower()
        all_students = self.get_all_students()
        results = []
        
        for student in all_students:
            # Поиск по имени
            if query_lower in student['name'].lower():
                results.append(student)
                continue
            
            # Поиск по названию работы
            thesis_title = student.get('thesis', {}).get('title', '')
            if query_lower in thesis_title.lower():
                results.append(student)
                continue
            
            # Поиск по аннотации
            thesis_summary = student.get('thesis', {}).get('summary', '')
            if query_lower in thesis_summary.lower():
                results.append(student)
                continue
            
            # Поиск по ключевым словам
            keywords = student.get('thesis', {}).get('keywords', [])
            if any(query_lower in keyword.lower() for keyword in keywords):
                results.append(student)
                continue
            
            # Поиск по научному руководителю
            advisor = student.get('thesis', {}).get('advisor', '')
            if query_lower in advisor.lower():
                results.append(student)
                continue
        
        return results
    
    def get_available_years(self) -> List[int]:
        """
        Получение списка доступных годов
        """
        years = []
        
        for year_dir in self.data_path.iterdir():
            if year_dir.is_dir() and year_dir.name.isdigit():
                year = int(year_dir.name)
                # Проверяем, что в году есть хотя бы один студент
                if any(self._load_student_info(year, student_dir.name) 
                       for student_dir in year_dir.iterdir() if student_dir.is_dir()):
                    years.append(year)
        
        return sorted(years, reverse=True)
    
    def get_student_code_file(self, student_id: str, filename: str) -> Optional[str]:
        """
        Получение содержимого файла кода студента
        """
        try:
            year_str, student_dir = student_id.split('_', 1)
            year = int(year_str)
            
            file_path = self.data_path / str(year) / student_dir / "code" / filename
            
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except (ValueError, IndexError, OSError):
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получение статистики по базе данных
        """
        all_students = self.get_all_students()
        years = self.get_available_years()
        
        stats = {
            'total_students': len(all_students),
            'total_years': len(years),
            'students_with_code': len([s for s in all_students if s.get('code', {}).get('has_code', False)]),
            'years_range': {
                'min': min(years) if years else None,
                'max': max(years) if years else None
            },
            'by_year': {}
        }
        
        # Статистика по годам
        for year in years:
            year_students = self.get_students_by_year(year)
            stats['by_year'][year] = {
                'count': len(year_students),
                'with_code': len([s for s in year_students if s.get('code', {}).get('has_code', False)])
            }
        
        return stats