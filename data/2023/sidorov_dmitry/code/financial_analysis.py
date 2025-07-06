import numpy as np
import random
import math
import json

def generate_stock_prices(n_days=100, initial_price=100, volatility=0.02, trend=0.001):
    """
    Генерирует синтетические цены акций с использованием модели случайного блуждания
    
    Args:
        n_days: количество дней
        initial_price: начальная цена
        volatility: волатильность (стандартное отклонение дневных изменений)
        trend: дневной тренд (средний рост)
    
    Returns:
        list: список цен по дням
    """
    prices = [initial_price]
    
    for i in range(n_days - 1):
        # Случайное изменение цены
        daily_return = random.normalvariate(trend, volatility)
        new_price = prices[-1] * (1 + daily_return)
        
        # Не даем цене стать отрицательной
        new_price = max(new_price, 0.01)
        prices.append(new_price)
    
    return prices

def calculate_returns(prices):
    """
    Вычисляет дневные доходности
    
    Args:
        prices: список цен
    
    Returns:
        list: список дневных доходностей
    """
    returns = []
    for i in range(1, len(prices)):
        daily_return = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(daily_return)
    
    return returns

def calculate_risk_metrics(returns):
    """
    Вычисляет метрики риска
    
    Args:
        returns: список доходностей
    
    Returns:
        dict: словарь с метриками риска
    """
    if not returns:
        return {}
    
    mean_return = sum(returns) / len(returns)
    
    # Волатильность (стандартное отклонение)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    volatility = math.sqrt(variance)
    
    # Коэффициент Шарпа (упрощенный, без безрисковой ставки)
    sharpe_ratio = mean_return / volatility if volatility > 0 else 0
    
    # Value at Risk (VaR) на уровне 95%
    sorted_returns = sorted(returns)
    var_95 = sorted_returns[int(0.05 * len(sorted_returns))]
    
    return {
        'mean_return': mean_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'var_95': var_95,
        'min_return': min(returns),
        'max_return': max(returns)
    }

def moving_average(prices, window=20):
    """
    Вычисляет скользящее среднее
    
    Args:
        prices: список цен
        window: размер окна
    
    Returns:
        list: скользящее среднее
    """
    if len(prices) < window:
        return prices[:]
    
    ma = []
    for i in range(window - 1, len(prices)):
        avg = sum(prices[i - window + 1:i + 1]) / window
        ma.append(avg)
    
    return ma

def detect_trend(prices, window=20):
    """
    Определяет тренд на основе скользящего среднего
    
    Args:
        prices: список цен
        window: размер окна для скользящего среднего
    
    Returns:
        str: 'up', 'down', или 'sideways'
    """
    if len(prices) < window * 2:
        return 'insufficient_data'
    
    ma = moving_average(prices, window)
    
    if len(ma) < 2:
        return 'insufficient_data'
    
    # Сравниваем последние значения скользящего среднего
    recent_trend = ma[-1] - ma[-min(10, len(ma))]
    
    if recent_trend > prices[-1] * 0.01:  # Рост более 1%
        return 'up'
    elif recent_trend < -prices[-1] * 0.01:  # Падение более 1%
        return 'down'
    else:
        return 'sideways'

def main(*args):
    """
    Главная функция для демонстрации финансового анализа
    
    Args:
        args: аргументы командной строки
            - n_days (int): количество дней (по умолчанию 100)
            - initial_price (float): начальная цена (по умолчанию 100)
            - volatility (float): волатильность (по умолчанию 0.02)
    """
    # Парсинг аргументов
    n_days = 100
    initial_price = 100.0
    volatility = 0.02
    
    if args:
        try:
            if len(args) >= 1:
                n_days = int(args[0])
            if len(args) >= 2:
                initial_price = float(args[1])
            if len(args) >= 3:
                volatility = float(args[2])
        except (ValueError, IndexError):
            print("Ошибка: неверные аргументы. Используйте: n_days, initial_price, volatility")
            return
    
    print(f"=== Анализ финансовых данных ===")
    print(f"Параметры: дней={n_days}, начальная цена={initial_price}, волатильность={volatility}")
    print()
    
    # Генерируем цены
    prices = generate_stock_prices(n_days, initial_price, volatility)
    
    print(f"Сгенерированы цены за {len(prices)} дней")
    print(f"Начальная цена: {prices[0]:.2f}")
    print(f"Конечная цена: {prices[-1]:.2f}")
    print(f"Изменение: {((prices[-1] / prices[0]) - 1) * 100:.2f}%")
    print()
    
    # Вычисляем доходности
    returns = calculate_returns(prices)
    
    # Анализ рисков
    risk_metrics = calculate_risk_metrics(returns)
    print("Метрики риска:")
    for metric, value in risk_metrics.items():
        if isinstance(value, float):
            print(f"  {metric}: {value:.6f}")
        else:
            print(f"  {metric}: {value}")
    print()
    
    # Скользящее среднее
    ma_20 = moving_average(prices, 20)
    print(f"Скользящее среднее (20 дней): {len(ma_20)} значений")
    if ma_20:
        print(f"  Последнее значение: {ma_20[-1]:.2f}")
    print()
    
    # Анализ тренда
    trend = detect_trend(prices, 20)
    trend_names = {
        'up': 'восходящий',
        'down': 'нисходящий', 
        'sideways': 'боковой',
        'insufficient_data': 'недостаточно данных'
    }
    print(f"Текущий тренд: {trend_names.get(trend, trend)}")
    
    print()
    print("=== Анализ завершен ===")
    
    return {
        'prices': prices[:10],  # Первые 10 цен для краткости
        'final_price': prices[-1],
        'total_return': ((prices[-1] / prices[0]) - 1) * 100,
        'risk_metrics': risk_metrics,
        'trend': trend,
        'moving_average_last': ma_20[-1] if ma_20 else None
    }

if __name__ == "__main__":
    import sys
    result = main(*sys.argv[1:])
    if result:
        print("\nРезультат в JSON формате:")
        print(json.dumps(result, ensure_ascii=False, indent=2))