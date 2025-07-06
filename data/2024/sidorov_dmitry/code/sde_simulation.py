"""
Стохастические дифференциальные уравнения в моделировании финансовых рынков
Автор: Сидоров Дмитрий Александрович
Год: 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class BlackScholesModel:
    """
    Модель Блэка-Шоулза для моделирования цены актива
    dS = μS dt + σS dW
    """
    
    def __init__(self, S0, mu, sigma):
        self.S0 = S0      # Начальная цена
        self.mu = mu      # Дрифт
        self.sigma = sigma # Волатильность
    
    def simulate_path(self, T, N):
        """
        Симуляция одного пути цены актива
        T - время до экспирации
        N - количество шагов
        """
        dt = T / N
        t = np.linspace(0, T, N+1)
        W = np.random.standard_normal(size=N+1)
        W = np.cumsum(W) * np.sqrt(dt)  # Броуновское движение
        W[0] = 0
        
        # Аналитическое решение
        S = self.S0 * np.exp((self.mu - 0.5 * self.sigma**2) * t + self.sigma * W)
        return t, S
    
    def monte_carlo_paths(self, T, N, num_paths):
        """
        Генерация множественных путей методом Монте-Карло
        """
        paths = []
        for _ in range(num_paths):
            t, S = self.simulate_path(T, N)
            paths.append(S)
        return t, np.array(paths)

class HestonModel:
    """
    Модель Хестона со стохастической волатильностью
    dS = μS dt + √v S dW1
    dv = κ(θ - v) dt + σ_v √v dW2
    """
    
    def __init__(self, S0, v0, mu, kappa, theta, sigma_v, rho):
        self.S0 = S0          # Начальная цена
        self.v0 = v0          # Начальная волатильность
        self.mu = mu          # Дрифт цены
        self.kappa = kappa    # Скорость возврата волатильности
        self.theta = theta    # Долгосрочная волатильность
        self.sigma_v = sigma_v # Волатильность волатильности
        self.rho = rho        # Корреляция между процессами
    
    def simulate_path(self, T, N):
        """
        Симуляция пути по модели Хестона методом Эйлера
        """
        dt = T / N
        t = np.linspace(0, T, N+1)
        
        # Коррелированные случайные процессы
        Z1 = np.random.standard_normal(N+1)
        Z2 = np.random.standard_normal(N+1)
        W1 = Z1
        W2 = self.rho * Z1 + np.sqrt(1 - self.rho**2) * Z2
        
        S = np.zeros(N+1)
        v = np.zeros(N+1)
        S[0] = self.S0
        v[0] = self.v0
        
        for i in range(N):
            # Обновление волатильности
            v[i+1] = v[i] + self.kappa * (self.theta - v[i]) * dt + \
                     self.sigma_v * np.sqrt(max(v[i], 0)) * np.sqrt(dt) * W2[i]
            v[i+1] = max(v[i+1], 0)  # Обеспечиваем неотрицательность
            
            # Обновление цены
            S[i+1] = S[i] + self.mu * S[i] * dt + \
                     np.sqrt(max(v[i], 0)) * S[i] * np.sqrt(dt) * W1[i]
        
        return t, S, v

def black_scholes_option_price(S, K, T, r, sigma, option_type='call'):
    """
    Аналитическая формула Блэка-Шоулза для цены опциона
    """
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    if option_type == 'call':
        price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:  # put
        price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
    
    return price

def monte_carlo_option_pricing(model, K, T, r, num_simulations=10000):
    """
    Оценка цены опциона методом Монте-Карло
    """
    payoffs = []
    
    for _ in range(num_simulations):
        t, S = model.simulate_path(T, 252)  # 252 торговых дня
        payoff = max(S[-1] - K, 0)  # Call option payoff
        payoffs.append(payoff)
    
    option_price = np.exp(-r * T) * np.mean(payoffs)
    return option_price, np.std(payoffs) / np.sqrt(num_simulations)

if __name__ == "__main__":
    # Параметры модели
    S0 = 100    # Начальная цена
    mu = 0.05   # Дрифт
    sigma = 0.2 # Волатильность
    T = 1.0     # Время до экспирации
    r = 0.03    # Безрисковая ставка
    K = 105     # Страйк опциона
    
    print("Моделирование финансовых рынков")
    print("=" * 40)
    
    # Модель Блэка-Шоулза
    bs_model = BlackScholesModel(S0, mu, sigma)
    
    # Симуляция путей
    t, paths = bs_model.monte_carlo_paths(T, 252, 100)
    
    # Визуализация
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    for i in range(min(20, len(paths))):
        plt.plot(t, paths[i], alpha=0.5)
    plt.title('Симуляция цены актива (модель Блэка-Шоулза)')
    plt.xlabel('Время')
    plt.ylabel('Цена')
    plt.grid(True)
    
    # Аналитическая цена опциона
    analytical_price = black_scholes_option_price(S0, K, T, r, sigma)
    
    # Цена опциона методом Монте-Карло
    mc_price, mc_std = monte_carlo_option_pricing(bs_model, K, T, r)
    
    print(f"Аналитическая цена call-опциона: {analytical_price:.4f}")
    print(f"Цена по Монте-Карло: {mc_price:.4f} ± {mc_std:.4f}")
    
    # Модель Хестона
    heston_model = HestonModel(
        S0=100, v0=0.04, mu=0.05, 
        kappa=2.0, theta=0.04, sigma_v=0.3, rho=-0.7
    )
    
    # Симуляция по модели Хестона
    t_h, S_h, v_h = heston_model.simulate_path(T, 252)
    
    plt.subplot(2, 2, 2)
    plt.plot(t_h, S_h)
    plt.title('Цена актива (модель Хестона)')
    plt.xlabel('Время')
    plt.ylabel('Цена')
    plt.grid(True)
    
    plt.subplot(2, 2, 3)
    plt.plot(t_h, v_h)
    plt.title('Стохастическая волатильность')
    plt.xlabel('Время')
    plt.ylabel('Волатильность')
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    final_prices = [path[-1] for path in paths]
    plt.hist(final_prices, bins=30, alpha=0.7, density=True)
    plt.title('Распределение финальных цен')
    plt.xlabel('Цена')
    plt.ylabel('Плотность')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()