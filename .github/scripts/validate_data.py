#!/usr/bin/env python3
"""
Скрипт для валидации данных студентов в PR
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

def validate_info_json(file_path: Path) -> List[str]:
    """Валидация файла info.json"""
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Некорректный JSON в {file_path}: {e}"]
    except Exception as e:
        return [f"Ошибка чтения файла {file_path}: {e}"]
    
    # Проверка обязательных полей
    required_fields = {
        'name': str,
        'email': str,
        'graduation_year': int,
        'thesis': dict,
        'code': dict
    }
    
    for field, field_type in required_fields.items():
        if field not in data:
            errors.append(f"Отсутствует обязательное поле '{field}' в {file_path}")
        elif not isinstance(data[field], field_type):
            errors.append(f"Поле '{field}' должно быть типа {field_type.__name__} в {file_path}")
    
    # Проверка полей thesis
    if 'thesis' in data and isinstance(data['thesis'], dict):
        thesis_required = {
            'title': str,
            'summary': str,
            'advisor': str,
            'keywords': list,
            'defense_date': str
        }
        
        for field, field_type in thesis_required.items():
            if field not in data['thesis']:
                errors.append(f"Отсутствует поле 'thesis.{field}' в {file_path}")
            elif not isinstance(data['thesis'][field], field_type):
                errors.append(f"Поле 'thesis.{field}' должно быть типа {field_type.__name__} в {file_path}")
    
    # Проверка полей code
    if 'code' in data and isinstance(data['code'], dict):
        code_required = {
            'has_code': bool,
            'main_file': (str, type(None)),
            'description': (str, type(None))
        }
        
        for field, field_types in code_required.items():
            if field not in data['code']:
                errors.append(f"Отсутствует поле 'code.{field}' в {file_path}")
            elif not isinstance(data['code'][field], field_types):
                type_names = [t.__name__ if t != type(None) else 'null' for t in (field_types if isinstance(field_types, tuple) else (field_types,))]
                errors.append(f"Поле 'code.{field}' должно быть одного из типов: {', '.join(type_names)} в {file_path}")
    
    # Проверка email
    if 'email' in data and isinstance(data['email'], str):
        if '@' not in data['email']:
            errors.append(f"Некорректный email в {file_path}")
    
    # Проверка года
    if 'graduation_year' in data and isinstance(data['graduation_year'], int):
        current_year = 2025
        if data['graduation_year'] < 2000 or data['graduation_year'] > current_year + 1:
            errors.append(f"Некорректный год выпуска в {file_path}: {data['graduation_year']}")
    
    # Проверка соответствия директории и года
    try:
        year_from_path = int(file_path.parent.parent.name)
        if 'graduation_year' in data and data['graduation_year'] != year_from_path:
            errors.append(f"Год в данных ({data['graduation_year']}) не соответствует директории ({year_from_path}) в {file_path}")
    except ValueError:
        errors.append(f"Некорректная структура директорий для {file_path}")
    
    return errors

def main():
    """Основная функция валидации"""
    data_dir = Path('data')
    if not data_dir.exists():
        print("Директория data не найдена")
        sys.exit(1)
    
    all_errors = []
    
    # Поиск всех файлов info.json
    for info_file in data_dir.rglob('info.json'):
        # Пропускаем файлы не в структуре год/студент/info.json
        parts = info_file.parts
        if len(parts) != 4 or parts[0] != 'data':
            continue
            
        year_dir = parts[1]
        student_dir = parts[2]
        
        # Проверяем, что год - это число
        try:
            int(year_dir)
        except ValueError:
            continue
        
        print(f"Проверка {info_file}...")
        errors = validate_info_json(info_file)
        all_errors.extend(errors)
    
    if all_errors:
        print("\n❌ Найдены ошибки валидации:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✅ Все файлы прошли валидацию!")

if __name__ == '__main__':
    main()