#!/usr/bin/env python3
"""
Скрипт для проверки структуры директорий
"""

import os
import sys
from pathlib import Path
import json

def check_directory_structure():
    """Проверка структуры директорий"""
    data_dir = Path('data')
    if not data_dir.exists():
        print("Директория data не найдена")
        return False
    
    errors = []
    
    for year_dir in data_dir.iterdir():
        if not year_dir.is_dir():
            continue
            
        # Проверяем, что имя директории - это год
        try:
            year = int(year_dir.name)
            if year < 2000 or year > 2030:
                errors.append(f"Некорректный год в названии директории: {year_dir.name}")
        except ValueError:
            # Пропускаем служебные файлы как README.md, TEMPLATE.md
            if year_dir.name not in ['README.md', 'TEMPLATE.md']:
                errors.append(f"Название директории должно быть годом: {year_dir.name}")
            continue
        
        # Проверяем студентов в году
        for student_dir in year_dir.iterdir():
            if not student_dir.is_dir():
                continue
                
            # Проверяем наличие info.json
            info_file = student_dir / 'info.json'
            if not info_file.exists():
                errors.append(f"Отсутствует файл info.json в {student_dir}")
                continue
            
            # Проверяем структуру имени директории студента
            if '_' not in student_dir.name:
                errors.append(f"Имя директории студента должно содержать подчеркивание: {student_dir.name}")
            
            # Проверяем соответствие кода
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                has_code = data.get('code', {}).get('has_code', False)
                main_file = data.get('code', {}).get('main_file')
                code_dir = student_dir / 'code'
                
                if has_code:
                    if not code_dir.exists():
                        errors.append(f"Указано has_code=true, но директория code отсутствует: {student_dir}")
                    elif main_file:
                        main_file_path = code_dir / main_file
                        if not main_file_path.exists():
                            errors.append(f"Основной файл кода не найден: {main_file_path}")
                
                # Проверяем, что нет лишних файлов
                allowed_items = {'info.json', 'thesis.pdf', 'code'}
                for item in student_dir.iterdir():
                    if item.name not in allowed_items:
                        errors.append(f"Неожиданный файл/директория: {item}")
                        
            except (json.JSONDecodeError, KeyError) as e:
                errors.append(f"Ошибка чтения info.json в {student_dir}: {e}")
    
    if errors:
        print("\n❌ Найдены ошибки структуры:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("\n✅ Структура директорий корректна!")
        return True

def main():
    """Основная функция"""
    if not check_directory_structure():
        sys.exit(1)

if __name__ == '__main__':
    main()