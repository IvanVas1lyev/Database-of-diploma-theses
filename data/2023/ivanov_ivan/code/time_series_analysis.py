import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

def generate_time_series(n_points=100, trend=0.1, noise_level=0.5, seasonal_period=12):
    """
    Генерирует синтетический временной ряд с трендом и сезонностью
    
    Args:
        n_points: количество точек во временном ряду
        trend: коэффициент тренда
        noise_level: уровень шума
        seasonal_period: период сезонности
    
    Returns:
        dict: словарь с временными метками и значениями
    """
    # Создаем временные метки
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(days=i*30) for i in range(n_points)]
    
    # Генерируем значения
    t = np.arange(n_points)
    
    # Тренд
    trend_component = trend * t
    
    # Сезонность
    seasonal_component = 2 * np.sin(2 * np.pi * t / seasonal_period)
    
    # Шум
    noise = np.random.normal(0, noise_level, n_points)
    
    # Итоговый ряд
    values = 10 + trend_component + seasonal_component + noise
    
    return {
        'dates': [d.strftime('%Y-%m-%d') for d in dates],
        'values': values.tolist(),
        'trend': trend,
        'seasonal_period': seasonal_period,
        'n_points': n_points
    }

def calculate_statistics(values):
    """
    Вычисляет основные статистики временного ряда
    
    Args:
        values: список значений временного ряда
    
    Returns:
        dict: словарь со статистиками
    """
    values = np.array(values)
    
    return {
        'mean': float(np.mean(values)),
        'std': float(np.std(values)),
        'min': float(np.min(values)),
        'max': float(np.max(values)),
        'median': float(np.median(values)),
        'trend_slope': float(np.polyfit(range(len(values)), values, 1)[0])
    }

def moving_average(values, window=5):
    """
    Вычисляет скользящее среднее
    
    Args:
        values: список значений
        window: размер окна
    
    Returns:
        list: скользящее среднее
    """
    values = np.array(values)
    if len(values) < window:
        return values.tolist()
    
    ma = np.convolve(values, np.ones(window)/window, mode='valid')
    return ma.tolist()

def main(*args):
    """
    Главная функция для демонстрации анализа временных рядов
    
    Args:
        args: аргументы командной строки
            - n_points (int): количество точек (по умолчанию 50)
            - trend (float): коэффициент тренда (по умолчанию 0.1)
            - window (int): размер окна для скользящего среднего (по умолчанию 5)
    """
    # Парсинг аргументов
    n_points = 50
    trend = 0.1
    window = 5
    
    if args:
        try:
            if len(args) >= 1:
                n_points = int(args[0])
            if len(args) >= 2:
                trend = float(args[1])
            if len(args) >= 3:
                window = int(args[2])
        except (ValueError, IndexError):
            print("Ошибка: неверные аргументы. Используйте: n_points, trend, window")
            return
    
    print(f"=== Анализ временных рядов ===")
    print(f"Параметры: точек={n_points}, тренд={trend}, окно={window}")
    print()
    
    # Генерируем временной ряд
    ts_data = generate_time_series(n_points=n_points, trend=trend)
    values = ts_data['values']
    
    print(f"Сгенерирован временной ряд из {len(values)} точек")
    print(f"Первые 5 значений: {[round(v, 2) for v in values[:5]]}")
    print()
    
    # Вычисляем статистики
    stats = calculate_statistics(values)
    print("Основные статистики:")
    for key, value in stats.items():
        print(f"  {key}: {round(value, 4)}")
    print()
    
    # Вычисляем скользящее среднее
    ma = moving_average(values, window=window)
    print(f"Скользящее среднее (окно={window}):")
    print(f"  Длина: {len(ma)} точек")
    print(f"  Первые 5 значений: {[round(v, 2) for v in ma[:5]]}")
    print()
    
    # Анализ тренда
    if abs(stats['trend_slope']) > 0.01:
        trend_direction = "возрастающий" if stats['trend_slope'] > 0 else "убывающий"
        print(f"Обнаружен {trend_direction} тренд (наклон: {stats['trend_slope']:.4f})")
    else:
        print("Тренд не обнаружен")
    
    print()
    print("=== Анализ завершен ===")
    
    return {
        'time_series': ts_data,
        'statistics': stats,
        'moving_average': ma[:10],  # Первые 10 значений для краткости
        'analysis': {
            'has_trend': abs(stats['trend_slope']) > 0.01,
            'trend_direction': 'up' if stats['trend_slope'] > 0 else 'down',
            'volatility': 'high' if stats['std'] > stats['mean'] * 0.2 else 'low'
        }
    }

if __name__ == "__main__":
    import sys
    result = main(*sys.argv[1:])
    if result:
        print("\nРезультат в JSON формате:")
        print(json.dumps(result, ensure_ascii=False, indent=2))