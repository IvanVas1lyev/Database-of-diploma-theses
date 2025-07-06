#!/usr/bin/env python3
"""
Скрипт для тестирования кода студентов
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path

def test_python_code(code_dir: Path, main_file: str) -> tuple[bool, str]:
    """Тестирование Python кода"""
    main_file_path = code_dir / main_file
    
    if not main_file_path.exists():
        return False, f"Основной файл не найден: {main_file_path}"
    
    # Проверяем синтаксис
    try:
        with open(main_file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        compile(code_content, str(main_file_path), 'exec')
    except SyntaxError as e:
        return False, f"Синтаксическая ошибка в {main_file_path}: {e}"
    except Exception as e:
        return False, f"Ошибка компиляции {main_file_path}: {e}"
    
    # Проверяем requirements.txt если есть
    requirements_file = code_dir / 'requirements.txt'
    if requirements_file.exists():
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                requirements = f.read().strip()
            
            # Проверяем формат requirements
            for line in requirements.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    # Базовая проверка формата пакета
                    if not any(op in line for op in ['==', '>=', '<=', '>', '<', '~=']):
                        return False, f"Некорректный формат в requirements.txt: {line}"
                        
        except Exception as e:
            return False, f"Ошибка чтения requirements.txt: {e}"
    
    # Пробуем импортировать основные модули (без выполнения)
    try:
        # Создаем временную директорию для тестирования
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Копируем файлы кода
            for file_path in code_dir.iterdir():
                if file_path.is_file() and file_path.suffix == '.py':
                    temp_file = temp_path / file_path.name
                    temp_file.write_text(file_path.read_text(encoding='utf-8'), encoding='utf-8')
            
            # Пробуем импортировать основной модуль
            module_name = main_file.replace('.py', '')
            test_script = f"""
import sys
sys.path.insert(0, '{temp_path}')
try:
    import {module_name}
    print("Import successful")
except ImportError as e:
    print(f"Import error: {{e}}")
    sys.exit(1)
except Exception as e:
    print(f"Other error: {{e}}")
    sys.exit(1)
"""
            
            result = subprocess.run([sys.executable, '-c', test_script], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return False, f"Ошибка импорта модуля: {result.stdout} {result.stderr}"
                
    except subprocess.TimeoutExpired:
        return False, "Тайм-аут при тестировании кода"
    except Exception as e:
        return False, f"Ошибка тестирования: {e}"
    
    return True, "Код прошел базовые проверки"

def main():
    """Основная функция тестирования"""
    data_dir = Path('data')
    if not data_dir.exists():
        print("Директория data не найдена")
        sys.exit(1)
    
    errors = []
    tested_count = 0
    
    # Поиск всех студентов с кодом
    for info_file in data_dir.rglob('info.json'):
        # Пропускаем файлы не в структуре год/студент/info.json
        parts = info_file.parts
        if len(parts) != 4 or parts[0] != 'data':
            continue
            
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            code_info = data.get('code', {})
            if not code_info.get('has_code', False):
                continue
                
            main_file = code_info.get('main_file')
            if not main_file:
                errors.append(f"Не указан main_file для {info_file}")
                continue
            
            code_dir = info_file.parent / 'code'
            if not code_dir.exists():
                errors.append(f"Директория code не найдена для {info_file}")
                continue
            
            print(f"Тестирование кода: {info_file.parent}")
            tested_count += 1
            
            success, message = test_python_code(code_dir, main_file)
            if not success:
                errors.append(f"Ошибка в коде {info_file.parent}: {message}")
            else:
                print(f"  ✅ {message}")
                
        except json.JSONDecodeError as e:
            errors.append(f"Некорректный JSON в {info_file}: {e}")
        except Exception as e:
            errors.append(f"Ошибка обработки {info_file}: {e}")
    
    print(f"\nПротестировано файлов с кодом: {tested_count}")
    
    if errors:
        print("\n❌ Найдены ошибки в коде:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✅ Все файлы кода прошли проверку!")

if __name__ == '__main__':
    main()